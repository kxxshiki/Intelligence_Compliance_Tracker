from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Drift(BaseModel):
    __tablename__ = "drift"

    control_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    asset_identifier: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    previous_evaluation_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    current_evaluation_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    previous_status: Mapped[str] = mapped_column(String(32), nullable=False)
    current_status: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
