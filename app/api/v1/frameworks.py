from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.framework_repository import FrameworkRepository

router = APIRouter()


@router.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    frameworks = FrameworkRepository(db).list()
    return [
        {
            "id": item.id,
            "name": item.name,
            "abbreviation": item.abbreviation,
            "version": item.version,
            "status": item.status,
            "description": item.description,
        }
        for item in frameworks
    ]


@router.get("/frameworks/{framework_id}")
def get_framework(framework_id: str, db: Session = Depends(get_db)):
    framework = FrameworkRepository(db).get_by_id(framework_id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return {
        "id": framework.id,
        "name": framework.name,
        "abbreviation": framework.abbreviation,
        "version": framework.version,
        "description": framework.description,
        "status": framework.status,
        "metadata": framework.metadata,
    }


@router.get("/frameworks/{framework_id}/controls")
def get_framework_controls(framework_id: str, db: Session = Depends(get_db)):
    framework = FrameworkRepository(db).get_by_id(framework_id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    controls = FrameworkRepository(db).get_control_records(framework_id)
    return {
        "framework_id": framework.id,
        "framework_name": framework.name,
        "controls": controls,
    }


@router.get("/frameworks/{framework_id}/summary")
def get_framework_summary(framework_id: str, db: Session = Depends(get_db)):
    framework = FrameworkRepository(db).get_by_id(framework_id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    controls = FrameworkRepository(db).get_control_records(framework_id)
    return {
        "framework_id": framework.id,
        "framework_name": framework.name,
        "total_controls": len(controls),
        "active_controls": sum(1 for item in controls if item.get("active") is True),
    }


@router.post("/frameworks", status_code=status.HTTP_201_CREATED)
def create_framework(payload: dict[str, Any], db: Session = Depends(get_db)):
    framework = FrameworkRepository(db).create(payload)
    return {"id": framework.id, "name": framework.name, "abbreviation": framework.abbreviation}
