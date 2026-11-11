from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.job_service import JobService

router = APIRouter()


@router.get("/jobs")
def list_jobs(status: str | None = Query(default=None), db: Session = Depends(get_db)):
    rows = JobService(db).repo.list(status=status)
    return [
        {
            "id": item.id,
            "name": item.name,
            "status": item.status,
            "started_at": item.started_at.isoformat() if item.started_at else None,
            "completed_at": item.completed_at.isoformat() if item.completed_at else None,
            "result_summary": item.result_summary,
            "error_message": item.error_message,
            "created_at": item.created_at.isoformat(),
        }
        for item in rows
    ]


@router.get("/scheduler/jobs")
def list_scheduler_jobs(status: str | None = Query(default=None), db: Session = Depends(get_db)):
    return list_jobs(status=status, db=db)


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
def create_job(name: str, db: Session = Depends(get_db)):
    job = JobService(db).create_job(name)
    return {"id": job.id, "name": job.name, "status": job.status}


@router.post("/scheduler/jobs", status_code=status.HTTP_201_CREATED)
def create_scheduler_job(name: str, db: Session = Depends(get_db)):
    return create_job(name=name, db=db)


@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = JobService(db).repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "name": job.name,
        "status": job.status,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "result_summary": job.result_summary,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat(),
    }


@router.get("/scheduler/jobs/{job_id}")
def get_scheduler_job(job_id: str, db: Session = Depends(get_db)):
    return get_job(job_id=job_id, db=db)


@router.post("/jobs/{job_id}/run")
def run_job(job_id: str, db: Session = Depends(get_db)):
    service = JobService(db)
    job = service.start_job(job_id)
    summary = f"Job {job.name} executed successfully."
    completed = service.complete_job(job.id, result_summary=summary)
    return {
        "id": completed.id,
        "name": completed.name,
        "status": completed.status,
        "result_summary": completed.result_summary,
    }
