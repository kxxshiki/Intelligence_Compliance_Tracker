from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.asset import Asset


class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, asset_id: str) -> Asset | None:
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def list(self, asset_type: str | None = None, status: str | None = None) -> list[Asset]:
        query = self.db.query(Asset)
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        if status:
            query = query.filter(Asset.status == status)
        return query.order_by(Asset.name).all()

    def create(self, payload: dict) -> Asset:
        sanitized = dict(payload)
        if "metadata" in sanitized and "metadata_" not in sanitized:
            sanitized["metadata_"] = sanitized.pop("metadata")
        asset = Asset(**sanitized)
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def update(self, asset: Asset, payload: dict) -> Asset:
        for field, value in payload.items():
            if field == "metadata":
                asset.metadata_ = value
            else:
                setattr(asset, field, value)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def archive(self, asset: Asset) -> Asset:
        asset.archived = True
        asset.status = "archived"
        self.db.commit()
        self.db.refresh(asset)
        return asset
