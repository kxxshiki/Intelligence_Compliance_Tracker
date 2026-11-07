from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.evidence import Evidence
from app.services.mapping_service import MappingService

router = APIRouter()


@router.get("/mappings/evidence/{evidence_id}")
def list_mappings_for_evidence(evidence_id: str, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if evidence is None:
        raise HTTPException(status_code=404, detail="Evidence not found")
    controls = MappingService(db).get_mapped_controls(evidence_id)
    return [{
        "control_id": control.control_id,
        "name": control.name,
        "category": control.category,
        "description": control.description,
        "status": "AUTO_MAPPED" if evidence.embedding and control.embedding else "REVIEW_REQUIRED",
    } for control in controls]
