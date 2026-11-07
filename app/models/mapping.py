from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class EvidenceControlMapping(BaseModel):
    __tablename__ = "mappings"

    evidence_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    mapping_status: Mapped[str] = mapped_column(String(32), nullable=False, default="REVIEW_REQUIRED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
