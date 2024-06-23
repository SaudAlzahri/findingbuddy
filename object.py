import os
from playsound import playsound
from ultralytics import YOLO
from clock import get_clock
import cv2
#from ultralytics.utils.plotting import Annotator ##draw on frame

from texttovoice import speak
import time
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
c=0
start = time.time()


# Function for getting depth based on length and width of the subject
def get_depth(length, width, subject, classes):
    if subject in classes:
        l_depth = round(classes[subject]["l_rate"]/length, 1)
        w_depth = round(classes[subject]["w_rate"]/width, 1)
        depth = round((l_depth + w_depth)/2, 1)
        print(str(depth) + "m")
        depth = round(depth)
        return (depth)

# Classes to be used, with depth rates relative to the camera, and actions
classes =  {
    'person': {'l_rate': 1600, 'w_rate': 600, 'action': 'land'},     
    'bicycle': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'car': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},'motorcycle': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'airplane': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'bus': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'train': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'truck': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'boat': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'traffic light': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'stop sign': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'parking meter': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},
    'bench': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'cat': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},
    'dog': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'backpack': {'l_rate': 400, 'w_rate': 400, 'action': 'grab'},
    'umbrella': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'},  
    'handbag': {'l_rate': 300, 'w_rate': 300, 'action': 'grab'}, 
    'tie': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
    'suitcase': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'},
    'sports ball': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
    'bottle': {'l_rate': 180, 'w_rate': 60, 'action': 'grab'},'cup': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'}, 
    'fork': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 'knife': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 
    'spoon': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 'bowl': {'l_rate': 77, 'w_rate': 160, 'action': 'grab'}, 
    'banana': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'}, 'apple': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'sandwich': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'}, 'orange': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'broccoli': {'l_rate': 50, 'w_rate': 50, 'action': 'grab'}, 'carrot': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'},
    'hot dog': {'l_rate': 100, 'w_rate': 60, 'action': 'grab'}, 'pizza': {'l_rate': 200, 'w_rate': 200, 'action': 'grab'},
    'donut': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'}, 'cake': {'l_rate': 250, 'w_rate': 250, 'action': 'grab'}, 
    'chair': {'l_rate': 760, 'w_rate': 640, 'action': 'land'}, 'couch': {'l_rate': 356, 'w_rate': 2000, 'action': 'land'}, 
    'potted plant': {'l_rate': 400, 'w_rate': 200, 'action': 'grab'}, 'bed': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'}, 
    'dining table': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'}, 'toilet': {'l_rate': 690, 'w_rate': 620, 'action': 'land'}, 
    'tv': {'l_rate': 640, 'w_rate': 1140, 'action': 'land'}, 'laptop': {'l_rate': 240, 'w_rate': 320, 'action': 'grab'},
    'mouse': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
    'remote': {'l_rate': 215, 'w_rate': 75, 'action': 'grab'},  
    'keyboard': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
    'cell phone': {'l_rate': 140, 'w_rate': 75, 'action': 'grab'}, 'microwave': {'l_rate': 290, 'w_rate': 540, 'action': 'grab'},
    'oven': {'l_rate': 580, 'w_rate': 580, 'action': 'land'}, 'toaster': {'l_rate': 220, 'w_rate': 330, 'action': 'grab'}, 
    'sink': {'l_rate': 200, 'w_rate': 380, 'action': 'land'}, 'refrigerator': {'l_rate': 1320, 'w_rate': 880, 'action': 'land'},
    'hair drier': {'l_rate': 290, 'w_rate': 250, 'action': 'grab'}, 'toothbrush': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 
}


 
# Function to detect objects in a video stream using YOLO and Mediapipe for hand tracking
def detect(model, vid, subject):
    loop = True
    start = time.time()
    c=cx=cy=timeout_counter=environment_counter=0
    objective=False
    with mp_hands.Hands(           
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
                while loop == True:
                    ret, image = vid.read()

                    objr_result = model(image)

                    cv2.imshow('Webcam', image)

                    #DETECT RIGHT HAND

                    image = cv2.cvtColor(cv2.flip(image, 1),cv2.COLOR_BGR2RGB)     

                    # To improve performance, optionally mark the image as not writeable to
                    # pass by reference.
                    image.flags.writeable = False
                    hand_result = hands.process(image)
                    image_height, image_width, _ = image.shape
                    

                    # Draw the hand annotations on the image (not needed)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    #environment feature settings (must be in this loop)
                    if subject == "environment":
                        environment_counter+=1
                        if environment_counter == 1:
                            speak("Detecting all objects in your environment.")
                        else: loop = False
                    
                    # Pick right hand       (still counts left when both hands are there... )
                    if hand_result.multi_handedness:
                        for i, m in enumerate(hand_result.multi_handedness):

                                for one in ((MessageToDict(m))['classification']):
                                    if (one['label']) == "Right":
                        
                                            c2=0
                                                # retrieve coordinates
                                            if hand_result.multi_hand_landmarks:
                                                for hand_landmarks in hand_result.multi_hand_landmarks:
                                                    # Getting coordinate 9      Coordinates are oriented in Quadrant IV
                                                    for ids, landmrk in enumerate(hand_landmarks.landmark):
                                                        cx, cy = int(abs((landmrk.x - 0.1) * image_width)), int(abs((landmrk.y + 0.2) * image_height))

                                                        
                                                        if ids == 9:
                                                            if c2 == 0:        #fix needed to ignore left hand when both hands in frame
                                                                
                                                                    #reformat coordinates
                                                                cx -= 590
                                                                cx  = -1*cx
                                                                cy -= 500
                                                                cy = -1*cy
                                                                
                                                                
                                                            
                                                                print ("RIGHT HAND\nX:", cx, "Y:", cy)
                                                                c2+=1
                    else: pass
                         

                    # Iterate through the results
                    no_results = True
                    for box, cls, conf in zip(objr_result[0].boxes.xyxy.tolist(), objr_result[0].boxes.cls.tolist(), objr_result[0].boxes.conf.tolist()):
                        no_results = False
                        x1, y1, x2, y2 = box

                            # reformat
                        x1, x2 = int(x1)-640, int(x2)-640
                        y1, y2 = int(y1)-360, int(y2)-360
                        width = abs(x1 - x2)
                        length = abs(y1 - y2)

                            # get center coordinates
                        x = (x2 + x1) // 2 
                        y = (y2 + y1) // 2

                        confidence = conf
                        detected_class = cls
                        name = objr_result[0].names[int(cls)]
                        print(name)

                            # get action
                                                
                        for object in classes:
                            if object == subject:
                                action = classes[object]['action']

                        #PARSE OBJECT RESULTS
                        if name == subject:    
                            print("reached here")
                            
                            #stops other detected objects from stopping code
                            objective = True

                            small_loop = True
                            while (time.time() - start) >=5 and small_loop == True:        #every 5 seconds, return results
                                print('detected'+subject+ 'at:  (' + str(x) + ", " + str(y) + ")")
                                depth = get_depth(length, width, subject, classes)
                                

                                timeout_counter +=1

                                if timeout_counter > 10:    #timeout system for results
                                    speak("TIME OUT! You may repeat your command to continue.")
                                    loop=False
                                
                                #modified clock result below (relative to hand) (!)
                                if action=='grab':      # subtracted 0.5m from grab (that is avg. relaxed armlength and the depth should be relative to the hand)
                                    speak(str(get_clock((x-cx), (y-cy))+", "+ str(depth - 0.5) + "m"))

                                    #STOP WHEN USER GRABS IT
                                    if depth < 0.7:
                                        loop = small_loop = False
                                        speak("Success! You can now grab the "+ str(subject))


                                else:  #(action == land)
                                    speak(str(get_clock(x, y)+", "+str(depth) + "m"))

                                    #STOP WHEN USER LANDS ON IT
                                    if depth < 2:
                                        loop = small_loop = False
                                        speak("Success! You have reached the " + str(subject))
    
                                start+=5

                            #use x, y to return clock direcitoning every 3 seconds
                        elif objective==False:
                             # for environment feature, objective == false
                             # therefore write if statement here, and if not environemnt feature, not detected outcome as usual
                            
                            if subject == "environment":
                                if environment_counter == 1:
                                    speak(name)
                            
                            else:
                                while (time.time() - start) >= 2 and c < 5:     #if object is not detected, continue running while beeping every second for 5 seconds
                                    print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
                                    #play beep sound
                                    playsound('beep.mp3')

                                    
                                    start+=2
                                    c+=1

                            if c==5:                                #after 5 seconds (can be longer) give not detected message and break
                                print("Not detected")
                                speak("Not detected")
                                c+=1
                                loop = False
                            #repeat search for 5 seconds until timeout (beep every second)
                    
                    if no_results:
                        while (time.time() - start) >= 5 and c < 3:
                            speak("The camera is not clear")
                            start+=5
                            c+=1

                        if c==3:
                            speak("FAILED. The camera may be blocked, or the room is too dark.")
                            loop = False

# Example of how to call the detect function
# detect(model, vid, "person")
