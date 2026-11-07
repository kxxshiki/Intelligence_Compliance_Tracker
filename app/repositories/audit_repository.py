from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log(self, event_type: str, entity_type: str, entity_id: str, metadata: dict | None = None) -> AuditLog:
        log = AuditLog(event_type=event_type, entity_type=entity_type, entity_id=entity_id, details=metadata or {})
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list(self, limit: int = 100) -> list[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
