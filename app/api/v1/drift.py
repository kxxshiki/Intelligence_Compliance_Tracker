from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.drift import Drift

router = APIRouter()


@router.get("/drift")
def list_drift(db: Session = Depends(get_db)):
    records = db.query(Drift).order_by(Drift.detected_at.desc()).all()
    return [{
        "id": item.id,
        "control_id": item.control_id,
        "asset_identifier": item.asset_identifier,
        "previous_status": item.previous_status,
        "current_status": item.current_status,
        "description": item.description,
    } for item in records]
