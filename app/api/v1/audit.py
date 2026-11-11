from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.audit_repository import AuditRepository

router = APIRouter()


@router.get("/audit/logs")
def list_audit_logs(
    entity_type: str | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    action: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
):
    rows = AuditRepository(db).list(
        entity_type=entity_type,
        entity_id=entity_id,
        event_type=action,
        start_date=start_date,
        end_date=end_date,
        limit=200,
    )
    return [
        {
            "id": item.id,
            "action": item.event_type,
            "entity_type": item.entity_type,
            "entity_id": item.entity_id,
            "details": item.details,
            "timestamp": item.timestamp.isoformat(),
        }
        for item in rows
    ]
