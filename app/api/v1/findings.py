from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.finding_repository import FindingRepository

router = APIRouter()


@router.get("/findings")
def list_findings(status: str | None = None, severity: str | None = None, control_id: str | None = None, db: Session = Depends(get_db)):
    findings = FindingRepository(db).list(status=status, severity=severity, control_id=control_id)
    return [{
        "id": item.id,
        "control_id": item.control_id,
        "asset_identifier": item.asset_identifier,
        "title": item.title,
        "severity": item.severity,
        "status": item.status,
        "description": item.description,
    } for item in findings]


@router.get("/findings/{finding_id}")
def get_finding(finding_id: str, db: Session = Depends(get_db)):
    finding = FindingRepository(db).get_by_id(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding


@router.patch("/findings/{finding_id}/status")
def patch_finding_status(finding_id: str, payload: dict, db: Session = Depends(get_db)):
    finding = FindingRepository(db).get_by_id(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    finding.status = payload.get("status", finding.status)
    if payload.get("status") == "REMEDIATED":
        finding.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(finding)
    return finding
