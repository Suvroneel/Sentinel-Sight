import cv2
import time

def start_stream(rtsp_url, callback):
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        if not cap.isOpened():
            time.sleep(2)
            cap.open(rtsp_url)

        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue

        callback(frame)
        time.sleep(0.1)
