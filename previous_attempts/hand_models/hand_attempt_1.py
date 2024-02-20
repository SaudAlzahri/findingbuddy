
# unsuccessful first attempt

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import cv2

model_path = '/Users/saud/Desktop/findingbuddy/hand_landmarker.task'


import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
with HandLandmarker.create_from_options(options) as landmarker:
  # The landmarker is initialized

    
    # define a video capture object 

    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10,150)




    # Create a loop to read the latest frame from the camera using opencv
    while cap.isOpened():

    # Capture the video frame
        success, frame = cap.read()



        if success:

        # Display the resulting frame
            cv2.imshow("Result", frame)
            


        # Convert the frame received from OpenCV to a MediaPipe’s Image object.

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame) ## frame must be numpy


        # Execute
            landmarker.detect_async(mp_image, int(time.time() * 1000))

        
        # Print





            # 'q' key quits the program
            #if cv2.waitKey(1) & 0xFF == ord('q'): 
             #   break
            
            break
        
cap.release() 
cv2.destroyAllWindows() 

