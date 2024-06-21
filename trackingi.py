
import threading
import cv2
from ultralytics import YOLO


frameWidth = 1280
frameHeight = 720
vid = cv2.VideoCapture(1)
vid.set(3, frameWidth)
vid.set(4, frameHeight)
vid.set(10,150)


model = YOLO('yolov8l.pt')

while True:
    ret, frame = vid.read()  # Read the video frames

    # Exit the loop if no more frames in either video
    if not ret:
        break

    # Track objects in frames if available
    results = model.track(frame, persist=True)

    print(results)
    res_plotted = results[0].plot()
    cv2.imshow(f"Tracking_Stream", res_plotted)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


