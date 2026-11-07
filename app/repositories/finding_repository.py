from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.finding import Finding


class FindingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, finding_id: str) -> Finding | None:
        return self.db.query(Finding).filter(Finding.id == finding_id).first()

    def list(self, status: str | None = None, severity: str | None = None, control_id: str | None = None) -> list[Finding]:
        query = self.db.query(Finding)
        if status:
            query = query.filter(Finding.status == status)
        if severity:
            query = query.filter(Finding.severity == severity)
        if control_id:
            query = query.filter(Finding.control_id == control_id)
        return query.order_by(Finding.last_detected_at.desc()).all()

    def create(self, payload: dict) -> Finding:
        finding = Finding(**payload)
        self.db.add(finding)
        self.db.commit()
        self.db.refresh(finding)
        return finding

    def update(self, finding: Finding, payload: dict) -> Finding:
        for field, value in payload.items():
            setattr(finding, field, value)
        finding.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(finding)
        return finding

    def find_open_for_asset_control(self, control_id: str, asset_identifier: str) -> Finding | None:
        return (
            self.db.query(Finding)
            .filter(
                Finding.control_id == control_id,
                Finding.asset_identifier == asset_identifier,
                Finding.status.notin_(["REMEDIATED", "CLOSED"]),
            )
            .order_by(Finding.last_detected_at.desc())
            .first()
        )
