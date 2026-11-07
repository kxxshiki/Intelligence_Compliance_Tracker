from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.asset_repository import AssetRepository

router = APIRouter()


@router.post("/assets", status_code=status.HTTP_201_CREATED)
def create_asset(payload: dict[str, Any], db: Session = Depends(get_db)):
    asset = AssetRepository(db).create(payload)
    return {
        "id": asset.id,
        "name": asset.name,
        "asset_type": asset.asset_type,
        "environment": asset.environment,
        "status": asset.status,
    }


@router.get("/assets")
def list_assets(
    asset_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    items = AssetRepository(db).list(asset_type=asset_type, status=status)
    return [
        {
            "id": item.id,
            "name": item.name,
            "asset_type": item.asset_type,
            "environment": item.environment,
            "owner": item.owner,
            "status": item.status,
            "metadata": item.metadata,
            "archived": item.archived,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }
        for item in items
    ]


@router.get("/assets/{asset_id}")
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = AssetRepository(db).get_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {
        "id": asset.id,
        "name": asset.name,
        "asset_type": asset.asset_type,
        "environment": asset.environment,
        "owner": asset.owner,
        "status": asset.status,
        "description": asset.description,
        "metadata": asset.metadata,
        "archived": asset.archived,
        "created_at": asset.created_at.isoformat(),
        "updated_at": asset.updated_at.isoformat(),
    }


@router.put("/assets/{asset_id}")
def update_asset(asset_id: str, payload: dict[str, Any], db: Session = Depends(get_db)):
    asset = AssetRepository(db).get_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    updated = AssetRepository(db).update(asset, payload)
    return {
        "id": updated.id,
        "name": updated.name,
        "asset_type": updated.asset_type,
        "status": updated.status,
    }


@router.delete("/assets/{asset_id}")
def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = AssetRepository(db).get_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    AssetRepository(db).archive(asset)
    return {"status": "archived", "id": asset_id}
