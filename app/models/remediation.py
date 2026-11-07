from __future__ import annotations

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Remediation(BaseModel):
    __tablename__ = "remediations"

    finding_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    asset_identifier: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_steps: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
