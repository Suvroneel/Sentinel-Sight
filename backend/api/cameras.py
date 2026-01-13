from fastapi import APIRouter
from backend.db import SessionLocal
from backend.models.camera import Camera

router = APIRouter()

@router.get("/")
def list_cameras():
    db = SessionLocal()
    return db.query(Camera).all()

@router.post("/")
def add_camera(camera: dict):
    db = SessionLocal()
    cam = Camera(**camera)
    db.add(cam)
    db.commit()
    return cam
