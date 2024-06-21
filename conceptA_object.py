
#    CONCEPT A

#
#
# selection of which of multiple similar looking objects the user wants.. (for example cans with different labels)
#
#
#
#


#
#   need to add object tracking model to create IDs for each object
#
#




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

from openai import OpenAI


import pyaudio
from vosk import Model, KaldiRecognizer
import json

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

    #classes to be used, with depth rates relative to camera, and action
classes =  {
    'person': {'l_rate': 1600, 'w_rate': 600, 'action': 'land'},     ##
    'bicycle': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'car': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},'motorcycle': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'airplane': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'bus': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'train': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'truck': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'boat': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'traffic light': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
    'stop sign': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'parking meter': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},
    'bench': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 'cat': {'l_rate': 00, 'w_rate': 00, 'action': 'land'},
    'dog': {'l_rate': 00, 'w_rate': 00, 'action': 'land'}, 
########################################
    'backpack': {'l_rate': 400, 'w_rate': 400, 'action': 'grab'},
    'umbrella': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'},  #-----------------DO THIS ONE##-----------------------#####
    'handbag': {'l_rate': 300, 'w_rate': 300, 'action': 'grab'}, 
    ##DO THESE  ##################
    'tie': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
    'suitcase': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'},
    'sports ball': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, 
########################################
    'bottle': {'l_rate': 180, 'w_rate': 60, 'action': 'grab'},'cup': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'}, 
    'fork': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 'knife': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 
    'spoon': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 'bowl': {'l_rate': 77, 'w_rate': 160, 'action': 'grab'}, 
########################################
    'banana': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'}, 'apple': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'sandwich': {'l_rate': 100, 'w_rate': 100, 'action': 'grab'}, 'orange': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'},
    'broccoli': {'l_rate': 50, 'w_rate': 50, 'action': 'grab'}, 'carrot': {'l_rate': 120, 'w_rate': 50, 'action': 'grab'},
    'hot dog': {'l_rate': 100, 'w_rate': 60, 'action': 'grab'}, 'pizza': {'l_rate': 200, 'w_rate': 200, 'action': 'grab'},
    'donut': {'l_rate': 70, 'w_rate': 70, 'action': 'grab'}, 'cake': {'l_rate': 250, 'w_rate': 250, 'action': 'grab'}, 
    'chair': {'l_rate': 760, 'w_rate': 640, 'action': 'land'}, 'couch': {'l_rate': 356, 'w_rate': 2000, 'action': 'land'}, 
    'potted plant': {'l_rate': 400, 'w_rate': 200, 'action': 'grab'}, 'bed': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'}, 
    'dining table': {'l_rate': 1200, 'w_rate': 2000, 'action': 'land'}, 'toilet': {'l_rate': 690, 'w_rate': 620, 'action': 'land'}, 
    'tv': {'l_rate': 640, 'w_rate': 1140, 'action': 'land'}, 'laptop': {'l_rate': 240, 'w_rate': 320, 'action': 'grab'},
    'mouse': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, #-----------------DO THIS ONE at home##-----------------------#####
    'remote': {'l_rate': 215, 'w_rate': 75, 'action': 'grab'},  
    'keyboard': {'l_rate': 00, 'w_rate': 00, 'action': 'grab'}, #-----------------DO THIS ONE at home##-----------------------#####
    'cell phone': {'l_rate': 140, 'w_rate': 75, 'action': 'grab'}, 'microwave': {'l_rate': 290, 'w_rate': 540, 'action': 'land'},
    'oven': {'l_rate': 580, 'w_rate': 580, 'action': 'land'}, 'toaster': {'l_rate': 220, 'w_rate': 330, 'action': 'land'}, 
##########################################
    'sink': {'l_rate': 200, 'w_rate': 380, 'action': 'land'}, 'refrigerator': {'l_rate': 1320, 'w_rate': 880, 'action': 'land'},
    'hair drier': {'l_rate': 290, 'w_rate': 250, 'action': 'grab'}, 'toothbrush': {'l_rate': 28, 'w_rate': 190, 'action': 'grab'}, 
}



# Load the YOLOv8 model
#model = YOLO('yolov8l.pt')

# Perform inference on an image

#vid = cv2.VideoCapture(1)  
 
def detect(model, vid, subject):
    loop = True
    start = time.time()
    c=cx=cy=r=0
    run_count = 1
    initial_count = {}
    objective=False
    with mp_hands.Hands(           #confidence settings set 50%
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
                while loop == True:
                    ret, image = vid.read()

                    objr_result = model(image)

                    #########DETECT RIGHT HAND
                    #annotator = Annotator(frame)   ##draw on frame
                    #frame = annotator.result()  

                    #cv2.imshow("f", frame)     ##open frame
                    # Flip the image horizontally for a later selfie-view display, and convert
                    # the BGR image to RGB.         (why??)

                    image = cv2.cvtColor(cv2.flip(image, 1),cv2.COLOR_BGR2RGB)     

                    # To improve performance, optionally mark the image as not writeable to
                    # pass by reference.
                    image.flags.writeable = False
                    hand_result = hands.process(image)
                    image_height, image_width, _ = image.shape
                    

                    # Draw the hand annotations on the image (not needed)
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
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

                        #Check in the beginning to see if there are multiple objects or not
                        if name == subject:
                            if run_count == 1:
                                r+=1
                                initial_count[str(name), "number", str(r)] = str((get_clock((x-cx), (y-cy))))
                            elif run_count == 2:   #After saving the initial results in initial count, ask the user which one he would like
                                if len(initial_count) > 1:
                                    print("There are", len(initial_count), str(name) + """s in front of you.""")
                                    speak("There are", len(initial_count), str(name) + """s in front of you.""")
                                    for object in initial_count:
                                        print(f"{object} which is {initial_count[object]} from your hand")
                                        speak(f"{object} which is {initial_count[object]} from your hand")


                                    ########NOW ALLOW USER TO RESPOND!######
                                    
                                    # Load the Vosk model
                                    model = Model("/Users/saud/Desktop/findingbuddy/success/vosk-model-small-en-us-0.15")

                                    # Initialize the recognizer with the model
                                    recognizer = KaldiRecognizer(model, 16000)



                                    speak("Which one would you like? Speak immediately.")
                                    save = ""  
                                            # Set up PyAudio
                                    p = pyaudio.PyAudio()
                                    stream = p.open(format=pyaudio.paInt16,
                                                    channels=1,
                                                    rate=16000,
                                                    input=True,
                                                    frames_per_buffer=4000)
                                    while True:
                                        try:
                                            data = stream.read(4000)
                                        except OSError:                 #open new audio stream when it was closed
                                            p = pyaudio.PyAudio()
                                            stream = p.open(format=pyaudio.paInt16,
                                                    channels=1,
                                                    rate=16000,
                                                    input=True,
                                                    frames_per_buffer=4000)
                                            
                                            data = stream.read(4000)
                                            save = ""              


                                        if len(data) == 0:
                                            break

                                        if recognizer.AcceptWaveform(data):
                                            result = recognizer.Result()
                                            data = json.loads(result)
                                            if "text" in data:

                                                if data["text"] == "":  #reset log once stops talking (delete previous commands)
                                                    save = ""


                                                    #add text recognized to log
                                                save += " " + data["text"]
                                                print(save)

                                                ###### Now summarizing user's response with ChatGPT ######

                                                client = OpenAI(api_key='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')
                                                stream = client.chat.completions.create(
                                                    model="gpt-3.5-turbo",
                                                    messages=[{"role": "user", "content": f"""A transcription model has recieved the following text from a user's dialogue. The user's dialougue is answering the question; "Would you like {name} number 1 or {name} number 2 or {name} number 3 etc... Please provide which {name} the user has said he wants (whether its {name} number 1 or {name} number 2 or {name} number 3 etc... ) by reading the transcription. Give the answer as the number only. Here is the transcription: {save}
                                                """}],
                                                    stream=True,
                                                )
                                                for chunk in stream:
                                                    if chunk.choices[0].delta.content is not None:
                                                        choice = chunk.choices[0].delta.content
                                                    else: 
                                                        pass
                                                
                                                print(choice)


                                    
                            
                            print("reached here")
                            
                            #stops other detected objects from stopping code
                            objective = True


                            while (time.time() - start) >=5:        #STOP WHEN USER GRABS IT (object coordinate relative to hand is 0,0)
                                print('detected'+subject+ 'at:  (' + str(x) + ", " + str(y) + ")")
                                depth =get_depth(length, width, subject, classes)
                                
                                #modified clock result below (relative to hand) (!)
                                if action=='grab':
                                    speak(str(get_clock((x-cx), (y-cy))+", "+depth))

                                else:
                                    speak(str(get_clock(x, y)+", "+depth))

                                start+=5
                                    ## NO TIMEOUT / GRAB, LAND STOP METHOD


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

                    run_count+=1
                    
                    if no_results:
                        while (time.time() - start) >= 5 and c < 3:
                            speak("The camera is not clear")
                            start+=5
                            c+=1

                        if c==3:
                            speak("FAILED. The camera may be blocked, or the room is too dark.")
                            loop = False



                
#detect(model, vid, "person")