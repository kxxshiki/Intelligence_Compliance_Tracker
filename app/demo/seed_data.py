from __future__ import annotations

from app.db.session import SessionLocal
from app.repositories.control_repository import ControlRepository


def seed_default_controls():
    db = SessionLocal()
    try:
        repo = ControlRepository(db)
        created = repo.seed_defaults()
        return repo.list() if created else repo.list()
    finally:
        db.close()
