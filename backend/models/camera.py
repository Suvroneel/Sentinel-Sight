from sqlalchemy import Column, String, Float
from backend.db import Base
import uuid

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    location = Column(String)
    rtsp_url = Column(String)
    status = Column(String, default="offline")
    fps = Column(Float, default=0.0)
    last_frame_ts = Column(String, nullable=True)
