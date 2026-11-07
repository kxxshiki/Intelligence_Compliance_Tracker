from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.control_repository import ControlRepository

router = APIRouter()


@router.post("/controls", status_code=status.HTTP_201_CREATED)
def create_control(payload: dict[str, Any], db: Session = Depends(get_db)):
    repo = ControlRepository(db)
    control = repo.create(payload)
    return {"id": control.id, "control_id": control.control_id, "name": control.name}


@router.get("/controls")
def list_controls(db: Session = Depends(get_db)):
    return [
        {
            "id": control.id,
            "control_id": control.control_id,
            "name": control.name,
            "framework": control.framework,
            "category": control.category,
            "severity": control.severity,
            "active": control.active,
        }
        for control in ControlRepository(db).list()
    ]


@router.get("/controls/{control_id}")
def get_control(control_id: str, db: Session = Depends(get_db)):
    control = ControlRepository(db).get_by_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control


@router.put("/controls/{control_id}")
def update_control(control_id: str, payload: dict[str, Any], db: Session = Depends(get_db)):
    control = ControlRepository(db).get_by_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    updated = ControlRepository(db).update(control, payload)
    return updated


@router.delete("/controls/{control_id}")
def delete_control(control_id: str, db: Session = Depends(get_db)):
    control = ControlRepository(db).get_by_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    ControlRepository(db).delete(control)
    return {"status": "deleted", "id": control_id}
