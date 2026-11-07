from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.evidence import Evidence
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.audit_service import AuditService
from app.services.evaluation_service import EvaluationService
from app.services.mapping_service import MappingService

router = APIRouter()


@router.post("/evaluations/evidence/{evidence_id}")
def evaluate_evidence(evidence_id: str, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if evidence is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    if not MappingService(db).get_mapped_controls(evidence_id):
        raise HTTPException(status_code=400, detail="Evidence has no mapped controls")
    results = EvaluationService(db).evaluate_evidence(evidence_id)
    AuditService(db).log_event("CONTROL_EVALUATED", "EVIDENCE", evidence_id, {"count": len(results)})
    return [{"id": item.id, "control_id": item.control_id, "status": item.status, "reason": item.reason} for item in results]


@router.get("/evaluations")
def list_evaluations(db: Session = Depends(get_db)):
    evaluations = EvaluationRepository(db).list()
    return [{
        "id": item.id,
        "control_id": item.control_id,
        "asset_identifier": item.asset_identifier,
        "status": item.status,
        "reason": item.reason,
        "evaluated_at": item.evaluated_at.isoformat(),
    } for item in evaluations]
