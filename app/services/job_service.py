from __future__ import annotations

from datetime import datetime, timezone

from app.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, db):
        self.db = db
        self.repo = JobRepository(db)

    def create_job(self, name: str):
        return self.repo.create(name)

    def start_job(self, job_id: str):
        job = self.repo.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")
        return self.repo.update(job, status="running", started_at=datetime.now(timezone.utc))

    def complete_job(self, job_id: str, result_summary: str | None = None, error_message: str | None = None):
        job = self.repo.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")
        status = "failed" if error_message else "completed"
        return self.repo.update(
            job,
            status=status,
            completed_at=datetime.now(timezone.utc),
            result_summary=result_summary,
            error_message=error_message,
        )
