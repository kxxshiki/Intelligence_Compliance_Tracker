from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/analytics/dashboard")
def analytics_dashboard(db: Session = Depends(get_db)):
    return AnalyticsService(db).dashboard()


@router.get("/analytics/compliance-score")
def compliance_score(db: Session = Depends(get_db)):
    return AnalyticsService(db).compliance_score()


@router.get("/analytics/control-summary")
def control_summary(db: Session = Depends(get_db)):
    return AnalyticsService(db).control_summary()


@router.get("/analytics/finding-summary")
def finding_summary(db: Session = Depends(get_db)):
    return AnalyticsService(db).finding_summary()


@router.get("/analytics/drift-summary")
def drift_summary(db: Session = Depends(get_db)):
    return AnalyticsService(db).drift_summary()


@router.get("/analytics/compliance-trends")
def compliance_trends(db: Session = Depends(get_db)):
    return AnalyticsService(db).compliance_trends()


@router.get("/analytics/finding-trends")
def finding_trends(db: Session = Depends(get_db)):
    return AnalyticsService(db).finding_trends()
