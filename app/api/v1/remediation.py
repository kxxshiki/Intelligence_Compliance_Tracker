from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.control import Control
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.repositories.finding_repository import FindingRepository
from app.services.remediation_service import RemediationService

router = APIRouter()


@router.post("/remediation/findings/{finding_id}")
def generate_grounded_remediation(finding_id: str, db: Session = Depends(get_db)):
    finding = FindingRepository(db).get_by_id(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    control = db.query(Control).filter(Control.control_id == finding.control_id).first()
    evidence = db.query(Evidence).filter(Evidence.asset_identifier == finding.asset_identifier).order_by(Evidence.collected_at.desc()).first()
    if control is None:
        raise HTTPException(status_code=404, detail="Control not found")
    result = RemediationService(db).generate_grounded_remediation(finding, control, evidence)
    return {"finding_id": finding_id, "remediation": result}


@router.post("/remediation/actions/{finding_id}")
def execute_action(finding_id: str, payload: dict, db: Session = Depends(get_db)):
    finding = FindingRepository(db).get_by_id(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    action = payload.get("action")
    if not action:
        raise HTTPException(status_code=400, detail="Action is required")
    result = RemediationService(db).execute_allowlisted_action(finding, action)
    return result
