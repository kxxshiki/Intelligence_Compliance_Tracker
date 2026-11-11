from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_name: str) -> Job:
        job = Job(name=job_name, status="pending")
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def list(self, status: str | None = None) -> list[Job]:
        query = self.db.query(Job)
        if status:
            query = query.filter(Job.status == status)
        return query.order_by(Job.created_at.desc()).all()

    def get_by_id(self, job_id: str) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def update(self, job: Job, **kwargs) -> Job:
        for field, value in kwargs.items():
            if value is not None:
                setattr(job, field, value)
        self.db.commit()
        self.db.refresh(job)
        return job
