from __future__ import annotations

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Framework(BaseModel):
    __tablename__ = "frameworks"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    abbreviation: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active", index=True)
    metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class FrameworkControl(BaseModel):
    __tablename__ = "framework_controls"

    framework_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    control_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    section: Mapped[str | None] = mapped_column(String(128), nullable=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
