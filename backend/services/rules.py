from datetime import datetime
import cv2
import uuid
from backend.models.event import Event
from backend.db import SessionLocal
from backend.services.event_bus import publish
from backend.services.event_bus import subscribe
from backend.services.rules import intrusion_rule

subscribe(intrusion_rule)

publish({
    "camera_id": camera_id,
    "detections": detections,
    "frame": frame
})

def intrusion_rule(camera_id, frame, detections):
    for det in detections:
        db = SessionLocal()
        snapshot_path = f"backend/static/snapshots/{uuid.uuid4()}.jpg"
        cv2.imwrite(snapshot_path, frame)

        evt = Event(
            camera_id=camera_id,
            timestamp=datetime.utcnow().isoformat(),
            rule="INTRUSION",
            object_type="person",
            confidence=det["conf"],
            snapshot_path=snapshot_path
        )
        db.add(evt)
        db.commit()
