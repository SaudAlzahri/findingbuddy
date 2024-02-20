import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import cv2


model_path = '/Users/saud/Desktop/findingbuddy/artificial_objects/model.tflite'



timestamp_ms = time.time()


    # webcam settings for Macbook's FacetimeHD Camera
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)



BaseOptions = mp.tasks.BaseOptions
DetectionResult = mp.tasks.components.containers.DetectionResult
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: DetectionResult, output_image: mp.Image, timestamp_ms: int):
    print('detection result: {}'.format(result))

options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path='/Users/saud/Desktop/findingbuddy/artificial_objects/model.tflite'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=5,
    result_callback=print_result)

with ObjectDetector.create_from_options(options) as detector:
  # The detector is initialized. Use it here.
  # ...
    


# Use OpenCV’s VideoCapture to start capturing from the webcam.

# Create a loop to read the latest frame from the camera using VideoCapture#read()

    while cap.isOpened():
        success, image = cap.read()

        if success:
            # Flip the image horizontally for a later selfie-view display, and convert
            image = cv2.flip(image, 1)        

    # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    # Send the latest frame to perform object detection.
    # Results are sent to the `result_callback` provided in the `ObjectDetectorOptions`.
            results = detector.detect_async(mp_image, mp.Timestamp.from_seconds(time.time()).value)
    
            cv2.imshow('MediaPipe Hands', mp_image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
cap.release()