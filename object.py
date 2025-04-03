import os
from playsound import playsound
from ultralytics import YOLO
from clock import get_clock
import cv2
import numpy as np
from texttovoice import speak
import time
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

# Initialize MediaPipe Hands (if needed for additional hand tracking)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Function to compute depth using the box dimensions and class-specific rates
def get_depth(length, width, subject, classes):
    if subject in classes:
        l_depth = round(classes[subject]["l_rate"] / length, 1) if length != 0 else 0
        w_depth = round(classes[subject]["w_rate"] / width, 1) if width != 0 else 0
        depth = round((l_depth + w_depth) / 2, 1)
        print(f"{depth}m")
        return depth
    return None

# Classes with depth rates and associated actions
classes = {
    'person': {'l_rate': 1600, 'w_rate': 600, 'action': 'land'},
    'bicycle': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'car': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'motorcycle': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'airplane': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'bus': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'train': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'truck': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'boat': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'traffic light': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'stop sign': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'parking meter': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'bench': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'cat': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'dog': {'l_rate': 0, 'w_rate': 0, 'action': 'land'},
    'backpack': {'l_rate': 400, 'w_rate': 400, 'action': 'grab'},
    'umbrella': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'handbag': {'l_rate': 300, 'w_rate': 300, 'action': 'grab'},
    'tie': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'suitcase': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'sports ball': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'bottle': {'l_rate': 180, 'w_rate': 60, 'action': 'grab'},
    'cup': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'},
    'fork': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'},
    'knife': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'},
    'spoon': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'},
    'bowl': {'l_rate': 77, 'w_rate': 160, 'action': 'grab'},
    'banana': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'},
    'apple': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'sandwich': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'},
    'orange': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'broccoli': {'l_rate': 50, 'w_rate': 50, 'action': 'grab'},
    'carrot': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'},
    'hot dog': {'l_rate': 100, 'w_rate': 60, 'action': 'grab'},
    'pizza': {'l_rate': 200, 'w_rate': 200, 'action': 'grab'},
    'donut': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'cake': {'l_rate': 250, 'w_rate': 250, 'action': 'grab'},
    'chair': {'l_rate': 760, 'w_rate': 640, 'action': 'land'},
    'couch': {'l_rate': 356, 'w_rate': 2000, 'action': 'land'},
    'potted plant': {'l_rate': 400, 'w_rate': 200, 'action': 'grab'},
    'bed': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'},
    'dining table': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'},
    'toilet': {'l_rate': 690, 'w_rate': 620, 'action': 'land'},
    'tv': {'l_rate': 640, 'w_rate': 1140, 'action': 'land'},
    'laptop': {'l_rate': 240, 'w_rate': 320, 'action': 'grab'},
    'mouse': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'remote': {'l_rate': 215, 'w_rate': 75, 'action': 'grab'},
    'keyboard': {'l_rate': 0, 'w_rate': 0, 'action': 'grab'},
    'cell phone': {'l_rate': 140, 'w_rate': 75, 'action': 'grab'},
    'microwave': {'l_rate': 290, 'w_rate': 540, 'action': 'land'},
    'oven': {'l_rate': 580, 'w_rate': 580, 'action': 'land'},
    'toaster': {'l_rate': 220, 'w_rate': 330, 'action': 'land'},
    'sink': {'l_rate': 200, 'w_rate': 380, 'action': 'land'},
    'refrigerator': {'l_rate': 1320, 'w_rate': 880, 'action': 'land'},
    'hair drier': {'l_rate': 290, 'w_rate': 250, 'action': 'grab'},
    'toothbrush': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'},
    'door': {'l_rate': 1500, 'w_rate': 900, 'action': 'land'},
}

# Load your YOLO model (e.g., yolov8l.pt)
model = YOLO("yolov8l.pt")

# Function to process a video stream: run detection, annotate frames (using the image-processing method), and provide speech feedback.
def detect(model, vid, subject):
    # Initialize a timer (for speech intervals) if needed
    last_speech_time = time.time()
    
    while True:
        ret, frame = vid.read()
        if not ret:
            break

        # (Optional) Correct camera rotation if required
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Run YOLO inference on the current frame
        results = model(frame)

        # Get frame dimensions and compute reference center offsets
        frame_height, frame_width, _ = frame.shape
        x_sub = int(frame_width / 2)
        y_sub = int(frame_height / 2)

        # Loop through each detection
        boxes = results[0].boxes.xyxy.tolist()
        classes_list = results[0].boxes.cls.tolist()
        confidences = results[0].boxes.conf.tolist()
        
        # For each detection, apply the image-based processing method
        for idx, (box, cls, conf) in enumerate(zip(boxes, classes_list, confidences)):
            # Convert box to individual coordinates
            # Also calculate adjusted coordinates for clock direction using the image-processing method
            x1, y1, x2, y2 = box
            x1_adj = int(x1) - x_sub
            x2_adj = int(x2) - x_sub
            y1_adj = int(y1) - y_sub
            y2_adj = int(y2) - y_sub
            width_adj = abs(x2_adj - x1_adj)
            length_adj = abs(y2_adj - y1_adj)
            x_center = (x1_adj + x2_adj) // 2
            y_center = (y1_adj + y2_adj) // 2
            # Invert y for clock calculation (as per your reference)
            y_center = -y_center

            # Get the original bounding box coordinates (as integers)
            left, top, right, bottom = map(int, box)
            box_width = right - left
            box_height = bottom - top

            # Retrieve the class name
            name = results[0].names[int(cls)]
            # Construct the label using get_clock and get_depth
            clock_dir = get_clock(x_center, y_center)
            depth_val = get_depth(box_height, box_width, name, classes)
            label = f"{name}: {clock_dir}, {depth_val}m"
            print(f"Detection {idx}: {label}")

            # Draw the bounding box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 6)
            # Draw a background rectangle for the label (the width is based on the length of the label string)
            cv2.rectangle(frame, (left - 3, top - 5), (left + round(len(label) * 11.7), top - 32), (0, 0, 0), -1)
            # Put the label text on the frame
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            # If the detected object matches the target subject, provide speech feedback every 5 seconds
            if name == subject and (time.time() - last_speech_time) >= 5:
                speak(label)
                last_speech_time = time.time()

        # Display the annotated frame
        cv2.imshow("Video Inference", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


