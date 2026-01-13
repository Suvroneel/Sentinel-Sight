from fastapi import APIRouter
from backend.db import SessionLocal
from backend.models.event import Event

router = APIRouter()

@router.get("/")
def list_events():
    db = SessionLocal()
    return db.query(Event).order_by(Event.timestamp.desc()).all()

@router.get("/{event_id}")
def get_event(event_id: str):
    db = SessionLocal()
    return db.query(Event).filter(Event.id == event_id).first()
