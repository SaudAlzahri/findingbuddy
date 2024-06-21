#NOTES FOR PROFESSOR
#
#       WORKS PERFECTLY
#
#   this is the main file hence the name 
#
#
# here we run audio recognition model ...
#
#
#
#    Here's VOSK Github: https://github.com/alphacep/vosk-api?tab=readme-ov-file
#
#     and documentation: https://alphacephei.com/vosk/
#
#
#
#               ... we then use the results from VOSK with 
#           the YOLOv8l model function called from object.py.
# 


#
import os
import sys
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import cv2
from ultralytics import YOLO
import nltk
from conceptB_object import detect
from texttovoice import speak

# function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'NN'



#
#
#
### UPDATE CLASSES HERE(BECAUSE YOU EDITED CLASSSES IN OBJECT FILE)
#     
classes = ['person','bicycle', 'car','motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',  'parking meter', 'bench',  'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',  'cup',  'fork', 'knife', 'spoon', 'bowl','banana','apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone','microwave', 'oven','toaster', 'sink', 'refrigerator',  'book', 'clock','vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
keywords = ['finding buddy', "finding body", 'filing buddy', 'filing body', 'find a buddy']
def find_command(text):
    for keyword in keywords:
        if keyword in text:
            text = text.split(keyword,1)[1]
            tokenized = nltk.word_tokenize(text)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
            return nouns





# load cv2, yolov8
yolo = YOLO('yolov8l.pt')

    # webcam settings for Macbook's FacetimeHD Camera
frameWidth = 1280
frameHeight = 720
vid = cv2.VideoCapture(0)
vid.set(3, frameWidth)
vid.set(4, frameHeight)
vid.set(10,150)


def close_stream(stream, p):
    stream.stop_stream()
    stream.close()
    p.terminate()


def live_speech_to_text():
    print("detect start")
    # Load the Vosk model
    model = Model("/Users/saud/Desktop/findingbuddy/success/vosk-model-small-en-us-0.15")

    # Initialize the recognizer with the model
    recognizer = KaldiRecognizer(model, 16000)



    print("Say something...")
    save = ""  
            # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)
    while True:
        object_feature = True   #for opting out of normal detection in case of environment feature
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

                nouns = find_command(save)
                subject_count=0

                if nouns != None:
                    
                    for noun in nouns:      #ENVIRONMENT FEATURE PATH
                        if noun == "environment" or noun == "environments":    # - add more similar sounding words
                            subject_count+=1
                            object_feature = False
                            close_stream(stream, p)
                            detect(yolo, vid, noun)
                            speak("Completed.")
                            
                
                    if object_feature == True:  #NORMAL PATH
                        for noun in nouns:              #make sure only one subject, if more count
                            if noun in classes:
                                subject_count+=1
                                print(noun + " was added to subject_count")
                            else:               #noun is not in a class
                                print(noun + " is not a detectable class")
                                speak(noun + " is not a detectable class")


                        if subject_count >1:
                            print("You have called for multiple objects: ")
                            speak("You have called for multiple objects: ")
                            for noun in nouns:
                                print(noun + " ")
                                speak(noun + " ")
                            print("Which object are you looking for? Repeat your command.")
                            speak("Which object are you looking for? Repeat your command.")
                            #immediately repeats after this (but user must say finding buddy again)
                        elif subject_count ==1:
                            for noun in nouns:  #only one noun
                                print("DETECTING" + noun)
                                speak("DETECTING " + noun)
                                close_stream(stream, p)
                                detect(yolo, vid, noun)
                            




                                
                                














live_speech_to_text()