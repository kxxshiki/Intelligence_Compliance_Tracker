from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import init_db
from app.demo.seed_data import seed_default_controls

app = FastAPI(title=settings.app_name, version="0.1.0", description="Intelligent Cyber Compliance Tracker backend MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

init_db()
seed_default_controls()


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@app.on_event("startup")
def startup_event():
    init_db()
    seed_default_controls()
