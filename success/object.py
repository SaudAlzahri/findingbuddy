#NOTES FOR PROFESSOR
#
#
#     yolov8l
#
# performs accurate OR on following 80 classes

#
#
#
#  https://docs.google.com/document/d/1GV9MF3nYtE3mQgIzHKKCnTPlkSaqZuqtJACAqcccch8/edit?usp=sharing
#
#
#
#
#       Note: X-axis may seem to be mirrored when running on laptop,
#             but this is caused because the laptop camera is facing 
#             the user, while device camera will be facing the other
#             way.

# And of course, heres the docs
#               https://docs.ultralytics.com/
#
# and heres the Github
#               https://github.com/ultralytics/ultralytics



import os
from playsound import playsound
from ultralytics import YOLO
from clock import get_clock
import cv2
#from ultralytics.utils.plotting import Annotator ##draw on frame

from texttovoice import speak
import time
c=0
start = time.time()

#print("LDSKFJ")

 # this shall be replaced by the audio to text


##function for getting depth
def get_depth(length, width, subject, classes):
    if subject in classes:
        l_depth = round(classes[subject]["l_rate"]/length, 1)
        w_depth = round(classes[subject]["w_rate"]/width, 1)
        depth = round((l_depth + w_depth)/2, 1)
        print(str(depth) + "m")
        return (str(depth) + " m")

    #classes to be used, with depth rates relative to camera
classes = {    
    'person': {'l_rate': 1600, 'w_rate': 600,},     ##
    'bicycle': {'l_rate': 00, 'w_rate': 00,}, 
    'car': {'l_rate': 00, 'w_rate': 00,},'motorcycle': {'l_rate': 00, 'w_rate': 00,}, 
    'airplane': {'l_rate': 00, 'w_rate': 00,}, 'bus': {'l_rate': 00, 'w_rate': 00,}, 
    'train': {'l_rate': 00, 'w_rate': 00,}, 'truck': {'l_rate': 00, 'w_rate': 00,}, 
    'boat': {'l_rate': 00, 'w_rate': 00,}, 'traffic light': {'l_rate': 00, 'w_rate': 00,}, 
    'stop sign': {'l_rate': 00, 'w_rate': 00,}, 'parking meter': {'l_rate': 00, 'w_rate': 00,},
    'bench': {'l_rate': 00, 'w_rate': 00,}, 'cat': {'l_rate': 00, 'w_rate': 00,},
    'dog': {'l_rate': 00, 'w_rate': 00,}, 
########################################
    'backpack': {'l_rate': 400, 'w_rate': 400,},
    'umbrella': {'l_rate': 00, 'w_rate': 00,},  #-----------------DO THIS ONE##-----------------------#####
    'handbag': {'l_rate': 300, 'w_rate': 300,}, 
    ##DO THESE  ##################
    'tie': {'l_rate': 00, 'w_rate': 00,}, 
    'suitcase': {'l_rate': 00, 'w_rate': 00,},
    'sports ball': {'l_rate': 00, 'w_rate': 00,}, 
########################################
    'bottle': {'l_rate': 180, 'w_rate': 60,},'cup': {'l_rate': 100, 'w_rate': 100,}, 
    'fork': {'l_rate': 28, 'w_rate': 190,}, 'knife': {'l_rate': 28, 'w_rate': 190,}, 
    'spoon': {'l_rate': 28, 'w_rate': 190,}, 'bowl': {'l_rate': 77, 'w_rate': 160,}, 
########################################
    'banana': {'l_rate': 120, 'w_rate': 50,}, 'apple': {'l_rate': 70, 'w_rate': 70,},
    'sandwich': {'l_rate': 100, 'w_rate': 100,}, 'orange': {'l_rate': 70, 'w_rate': 70,},
    'broccoli': {'l_rate': 50, 'w_rate': 50,}, 'carrot': {'l_rate': 120, 'w_rate': 50,},
    'hot dog': {'l_rate': 100, 'w_rate': 60,}, 'pizza': {'l_rate': 200, 'w_rate': 200,},
    'donut': {'l_rate': 70, 'w_rate': 70,}, 'cake': {'l_rate': 250, 'w_rate': 250,}, 
    'chair': {'l_rate': 760, 'w_rate': 640,}, 'couch': {'l_rate': 356, 'w_rate': 2000,}, 
    'potted plant': {'l_rate': 400, 'w_rate': 200,}, 'bed': {'l_rate': 1200, 'w_rate': 2000,}, 
    'dining table': {'l_rate': 1200, 'w_rate': 2000,}, 'toilet': {'l_rate': 690, 'w_rate': 620,}, 
    'tv': {'l_rate': 640, 'w_rate': 1140,}, 'laptop': {'l_rate': 240, 'w_rate': 320,},
    'mouse': {'l_rate': 00, 'w_rate': 00,}, #-----------------DO THIS ONE at home##-----------------------#####
    'remote': {'l_rate': 215, 'w_rate': 75,},  
    'keyboard': {'l_rate': 00, 'w_rate': 00,}, #-----------------DO THIS ONE at home##-----------------------#####
    'cell phone': {'l_rate': 140, 'w_rate': 75,}, 'microwave': {'l_rate': 290, 'w_rate': 540,},
    'oven': {'l_rate': 580, 'w_rate': 580,}, 'toaster': {'l_rate': 220, 'w_rate': 330,}, 
##########################################
    'sink': {'l_rate': 200, 'w_rate': 380,}, 'refrigerator': {'l_rate': 1320, 'w_rate': 880,},
    'hair drier': {'l_rate': 290, 'w_rate': 250,}, 'toothbrush': {'l_rate': 28, 'w_rate': 190} 
}







# Load the YOLOv8 model
#model = YOLO('yolov8l.pt')

# Perform inference on an image

#vid = cv2.VideoCapture(1)  
 
def detect(model, vid, subject):
    loop = True
    start = time.time()
    c=0
    objective=False
    while loop == True:
        ret, frame = vid.read()

        results = model(frame)


        #annotator = Annotator(frame)   ##draw on frame
        #frame = annotator.result()  

        #cv2.imshow("f", frame)     ##open frame



        # Iterate through the results
        no_results = True

        for box, cls, conf in zip(results[0].boxes.xyxy.tolist(), results[0].boxes.cls.tolist(), results[0].boxes.conf.tolist()):
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
            name = results[0].names[int(cls)]
            print(name)

            if name == subject:
                print("reached here")
                
                #stops other detected objects from stopping code
                objective = True


                while (time.time() - start) >=5:        #STOP WHEN USER GRABS IT (object coordinate relative to hand is 0,0)
                    print('detected'+subject+ 'at:  (' + str(x) + ", " + str(y) + ")")
                    depth =get_depth(length, width, subject, classes)
                    speak(str(get_clock(x, y))+", "+depth)
                    start+=5



                #use x, y to return clock direcitoning every 3 seconds
            elif objective==False:
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


#detect(model, vid, "person")