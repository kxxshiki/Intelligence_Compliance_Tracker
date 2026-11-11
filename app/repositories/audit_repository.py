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

    def list(
        self,
        *,
        entity_type: str | None = None,
        entity_id: str | None = None,
        event_type: str | None = None,
        start_date=None,
        end_date=None,
        limit: int = 100,
    ) -> list[AuditLog]:
        query = self.db.query(AuditLog)
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        if event_type:
            query = query.filter(AuditLog.event_type == event_type)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
