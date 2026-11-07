from __future__ import annotations

import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.background.evidence_processor import process_evidence
from app.repositories.audit_repository import AuditRepository
from app.repositories.evidence_repository import EvidenceRepository

router = APIRouter()


@router.post("/evidence", status_code=status.HTTP_201_CREATED)
def create_evidence(payload: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    evidence_data = payload.get("raw_data", payload)
    evidence_hash = hashlib.sha256(json.dumps(evidence_data, sort_keys=True).encode("utf-8")).hexdigest()
    evidence = EvidenceRepository(db).create({
        "source_type": payload.get("source_type", "USER"),
        "source_name": payload.get("source_name", "manual"),
        "asset_identifier": payload.get("asset_identifier", payload.get("username") or payload.get("repository") or payload.get("server") or "unknown"),
        "evidence_type": payload.get("evidence_type", "USER_SECURITY_CONFIGURATION"),
        "raw_data": evidence_data,
        "normalized_data": None,
        "evidence_hash": evidence_hash,
        "processing_status": "PENDING",
        "collected_at": datetime.utcnow(),
    })
    AuditRepository(db).log("EVIDENCE_COLLECTED", "EVIDENCE", evidence.id, {"hash": evidence_hash})
    background_tasks.add_task(process_evidence, evidence.id)
    return {"id": evidence.id, "evidence_hash": evidence_hash, "status": evidence.processing_status}


@router.get("/evidence")
def list_evidence(db: Session = Depends(get_db)):
    return [
        {
            "id": item.id,
            "asset_identifier": item.asset_identifier,
            "source_type": item.source_type,
            "evidence_type": item.evidence_type,
            "processing_status": item.processing_status,
            "evidence_hash": item.evidence_hash,
        }
        for item in EvidenceRepository(db).list()
    ]


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str, db: Session = Depends(get_db)):
    evidence = EvidenceRepository(db).get_by_id(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return {
        "id": evidence.id,
        "source_type": evidence.source_type,
        "source_name": evidence.source_name,
        "asset_identifier": evidence.asset_identifier,
        "evidence_type": evidence.evidence_type,
        "raw_data": evidence.raw_data,
        "normalized_data": evidence.normalized_data,
        "evidence_hash": evidence.evidence_hash,
        "processing_status": evidence.processing_status,
        "collected_at": evidence.collected_at.isoformat(),
    }
