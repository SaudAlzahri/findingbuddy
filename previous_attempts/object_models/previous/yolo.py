
## DEFAULT MODEL

import torch
import cv2



# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

    # webcam settings for Macbook's FacetimeHD Camera
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

while cap.isOpened():
    success, image = cap.read()

    if success:

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)
         
# Inference
        results = model(image)


# Results
        #results.print()
        cv2.imshow("window", results)

        if cv2.waitKey(5) & 0xFF == 27:
                break
cap.release()