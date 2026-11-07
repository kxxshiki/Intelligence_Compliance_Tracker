from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.constants import CONTROL_SEED
from app.models.control import Control


class ControlRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, control_id: str) -> Control | None:
        return self.db.query(Control).filter(Control.id == control_id).first()

    def get_by_control_id(self, control_id: str) -> Control | None:
        return self.db.query(Control).filter(Control.control_id == control_id).first()

    def list(self, framework: str | None = None, category: str | None = None, active: bool | None = None) -> list[Control]:
        query = self.db.query(Control)
        if framework:
            query = query.filter(Control.framework == framework)
        if category:
            query = query.filter(Control.category == category)
        if active is not None:
            query = query.filter(Control.active == active)
        return query.order_by(Control.control_id).all()

    def create(self, payload: dict) -> Control:
        control = Control(**payload)
        self.db.add(control)
        self.db.commit()
        self.db.refresh(control)
        return control

    def update(self, control: Control, payload: dict) -> Control:
        for field, value in payload.items():
            setattr(control, field, value)
        self.db.commit()
        self.db.refresh(control)
        return control

    def delete(self, control: Control) -> None:
        self.db.delete(control)
        self.db.commit()

    def seed_defaults(self) -> list[Control]:
        created: list[Control] = []
        for item in CONTROL_SEED:
            if not self.get_by_control_id(item["control_id"]):
                control = self.create({**item, "active": True})
                created.append(control)
        return created
