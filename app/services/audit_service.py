from __future__ import annotations

from app.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db):
        self.db = db
        self.repo = AuditRepository(db)

    def log_event(self, event_type: str, entity_type: str, entity_id: str, metadata: dict | None = None):
        return self.repo.log(event_type, entity_type, entity_id, metadata or {})
