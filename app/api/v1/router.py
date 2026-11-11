from fastapi import APIRouter

from app.api.v1 import (
    analytics,
    assets,
    audit,
    controls,
    demo,
    drift,
    evidence,
    evaluations,
    findings,
    frameworks,
    health,
    jobs,
    mappings,
    remediation,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(assets.router, tags=["assets"])
api_router.include_router(frameworks.router, tags=["frameworks"])
api_router.include_router(controls.router, tags=["controls"])
api_router.include_router(evidence.router, tags=["evidence"])
api_router.include_router(evaluations.router, tags=["evaluations"])
api_router.include_router(findings.router, tags=["findings"])
api_router.include_router(drift.router, tags=["drift"])
api_router.include_router(mappings.router, tags=["mappings"])
api_router.include_router(remediation.router, tags=["remediation"])
api_router.include_router(analytics.router, tags=["analytics"])
api_router.include_router(audit.router, tags=["audit"])
api_router.include_router(jobs.router, tags=["jobs"])
api_router.include_router(demo.router, prefix="/demo", tags=["demo"])
