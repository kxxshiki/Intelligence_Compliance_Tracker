from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.control import Control
from app.models.framework import Framework, FrameworkControl


class FrameworkRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Framework]:
        return self.db.query(Framework).order_by(Framework.name).all()

    def get_by_id(self, framework_id: str) -> Framework | None:
        return self.db.query(Framework).filter(Framework.id == framework_id).first()

    def get_framework_controls(self, framework_id: str) -> list[FrameworkControl]:
        return self.db.query(FrameworkControl).filter(FrameworkControl.framework_id == framework_id).all()

    def map_control(self, framework_id: str, control_id: str, section: str | None = None, category: str | None = None, notes: str | None = None) -> FrameworkControl:
        existing = self.db.query(FrameworkControl).filter(FrameworkControl.framework_id == framework_id, FrameworkControl.control_id == control_id).first()
        if existing:
            return existing
        mapping = FrameworkControl(framework_id=framework_id, control_id=control_id, section=section, category=category, notes=notes)
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def create(self, payload: dict) -> Framework:
        framework = Framework(**payload)
        self.db.add(framework)
        self.db.commit()
        self.db.refresh(framework)
        return framework

    def get_control_records(self, framework_id: str) -> list[dict]:
        mappings = self.get_framework_controls(framework_id)
        controls = self.db.query(Control).filter(Control.control_id.in_([item.control_id for item in mappings])).all()
        control_map = {control.control_id: control for control in controls}
        rows: list[dict] = []
        for mapping in mappings:
            control = control_map.get(mapping.control_id)
            rows.append({
                "framework_id": mapping.framework_id,
                "control_id": mapping.control_id,
                "name": control.name if control else None,
                "section": mapping.section,
                "category": mapping.category,
                "severity": control.severity if control else None,
                "active": control.active if control else None,
            })
        return rows
