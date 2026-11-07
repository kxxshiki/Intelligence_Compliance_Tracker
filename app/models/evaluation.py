from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Evaluation(BaseModel):
    __tablename__ = "evaluations"

    control_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    asset_identifier: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    evaluation_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
