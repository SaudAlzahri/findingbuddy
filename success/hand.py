#NOTES FOR PROFESSOR
#
# Second attempt success
#
#
#           This file is kept on the side from now. It accurately
#       implements hand recognition model from Mediapipe.
#
#
#
#          This can be used later when building hand-relative 
#       results for the blind person.
#
#



# heres the docs
#               https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python
#
# and heres the Github
#               https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md


import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
import time

    # webcam settings for Macbook's FacetimeHD Camera
frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

with mp_hands.Hands(           #confidence settings set 50%
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  
  while cap.isOpened():
    success, image = cap.read()

    if success:
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.         (why??)

        image = cv2.cvtColor(cv2.flip(image, 1),cv2.COLOR_BGR2RGB)     

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)
        image_height, image_width, _ = image.shape
        

        # Draw the hand annotations on the image (not needed)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Pick right hand       (still counts left when both hands are there... )
        if results.multi_handedness:
            for i, m in enumerate(results.multi_handedness):

                    for one in ((MessageToDict(m))['classification']):
                        if (one['label']) == "Right":
            
                                c=0
                                    # retrieve coordinates
                                if results.multi_hand_landmarks:
                                    for hand_landmarks in results.multi_hand_landmarks:
                                        # Getting coordinate 9      Coordinates are oriented in Quadrant IV
                                        for ids, landmrk in enumerate(hand_landmarks.landmark):
                                            cx, cy = int(abs((landmrk.x - 0.1) * image_width)), int(abs((landmrk.y + 0.2) * image_height))

                                            
                                            if ids == 9:
                                                if c == 0:        #fix needed to ignore left hand when both hands in frame
                                                    
                                                        #reformat coordinates
                                                    cx -= 590
                                                    cx  = -1*cx
                                                    cy -= 500
                                                    cy = -1*cy
                                                    
                                                    
                                                
                                                    print ("X:", cx, "Y:", cy)
                                                    c+=1
                

                                            # NOT NEEDED 
                                        mp_drawing.draw_landmarks(
                                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # NOT NEEDED EITHER
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
cap.release()