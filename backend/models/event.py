from sqlalchemy import Column, String, Float
from backend.db import Base
import uuid

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    camera_id = Column(String)
    timestamp = Column(String)
    rule = Column(String)
    object_type = Column(String)
    confidence = Column(Float)
    snapshot_path = Column(String)
