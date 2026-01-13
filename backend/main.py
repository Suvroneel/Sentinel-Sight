from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api import cameras, events, health
from backend.db import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app FIRST
app = FastAPI(title="SentinelSight")

# Routers
app.include_router(cameras.router, prefix="/cameras")
app.include_router(events.router, prefix="/events")
app.include_router(health.router)

# Static files (snapshots + UI)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

@app.get("/api")
def api_root():
    return {"status": "SentinelSight API running"}
