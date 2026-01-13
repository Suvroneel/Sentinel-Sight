from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect(frame):
    results = model(frame, classes=[0])  # person
    detections = []

    for r in results:
        for box in r.boxes:
            detections.append({
                "bbox": box.xyxy.tolist()[0],
                "conf": float(box.conf)
            })

    return detections
