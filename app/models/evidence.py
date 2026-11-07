from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, embedding_column


class Evidence(BaseModel):
    __tablename__ = "evidence"

    source_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_identifier: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    normalized_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    evidence_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    processing_status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING", index=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    embedding: Mapped[list | None] = embedding_column()
