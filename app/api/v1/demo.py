from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.background.evidence_processor import process_evidence
from app.demo.seed_data import seed_default_controls
from app.demo.simulated_environment import SimulatedEnvironment
from app.repositories.audit_repository import AuditRepository
from app.repositories.evidence_repository import EvidenceRepository

router = APIRouter()


@router.post("/seed")
def demo_seed(db: Session = Depends(get_db)):
    created = seed_default_controls()
    return {"status": "seeded", "count": len(created)}


@router.post("/collect-evidence")
def demo_collect_evidence(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    environment = SimulatedEnvironment()
    items = environment.collect_evidence()
    for item in items:
        evidence = EvidenceRepository(db).create({
            "source_type": item["source_type"],
            "source_name": item["source_name"],
            "asset_identifier": item["asset_identifier"],
            "evidence_type": item["evidence_type"],
            "raw_data": item["raw_data"],
            "normalized_data": None,
            "evidence_hash": hashlib.sha256(json.dumps(item["raw_data"], sort_keys=True).encode("utf-8")).hexdigest(),
            "processing_status": "PENDING",
            "collected_at": datetime.utcnow(),
        })
        AuditRepository(db).log("EVIDENCE_COLLECTED", "EVIDENCE", evidence.id, {"asset": evidence.asset_identifier})
        background_tasks.add_task(process_evidence, evidence.id)
    return {"status": "collected", "count": len(items)}


@router.post("/run-compliance-check")
def demo_run_compliance_check(db: Session = Depends(get_db)):
    evidence = db.query(__import__('app.models.evidence', fromlist=['Evidence']).Evidence).order_by(__import__('app.models.evidence', fromlist=['Evidence']).Evidence.collected_at.desc()).first()
    if evidence is None:
        raise HTTPException(status_code=404, detail="No evidence available")
    asyncio.run(process_evidence(evidence.id))
    return {"status": "processed", "evidence_id": evidence.id}


@router.post("/simulate-drift")
def demo_simulate_drift(db: Session = Depends(get_db)):
    environment = SimulatedEnvironment()
    environment.drift_example()
    items = environment.collect_evidence()
    for item in items:
        evidence = EvidenceRepository(db).create({
            "source_type": item["source_type"],
            "source_name": item["source_name"],
            "asset_identifier": item["asset_identifier"],
            "evidence_type": item["evidence_type"],
            "raw_data": item["raw_data"],
            "normalized_data": None,
            "evidence_hash": hashlib.sha256(json.dumps(item["raw_data"], sort_keys=True).encode("utf-8")).hexdigest(),
            "processing_status": "PENDING",
            "collected_at": datetime.utcnow(),
        })
        asyncio.run(process_evidence(evidence.id))
    return {"status": "drift-simulated"}
