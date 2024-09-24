import os
import sys
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import cv2
from ultralytics import YOLO
import nltk
from object import detect
from texttovoice import speak
from pathlib import Path

# Necessary NLTK Downloads
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('taggers/averaged_perceptron_tagger_eng/')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'NN'

# Update classes here (because you edited classes in object file)
classes = ['person','bicycle', 'car','motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 
           'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 
           'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 
           'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 
           'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl','banana','apple', 
           'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 
           'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
           'cell phone','microwave', 'oven','toaster', 'sink', 'refrigerator', 'book', 'clock','vase', 'scissors', 
           'teddy bear', 'hair drier', 'toothbrush']

keywords = ['finding buddy', "finding body", 'filing buddy', 'filing body', 'find a buddy', 'finding a buddy']

def find_command(text):
    for keyword in keywords:
        if keyword in text:
            text = text.split(keyword, 1)[1]
            tokenized = nltk.word_tokenize(text)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
            return nouns

# Load YOLO model
yolo = YOLO('yolov8l.pt')

# Webcam settings for Iriun Webcam free plan (resolution is 720p)
frameWidth = 1280
frameHeight = 720
vid = cv2.VideoCapture(0)  # Value 0 should default to Iriun Webcam, otherwise try 1 or 2
vid.set(3, frameWidth)
vid.set(4, frameHeight)
vid.set(10, 150)

def close_stream(stream, p):
    stream.stop_stream()
    stream.close()
    p.terminate()

def live_speech_to_text():
    print("Detect start")
    # Load the Vosk model
    model = Model(str(Path("vosk-model-small-en-us-0.15").resolve()))

    # Initialize the recognizer with the model
    recognizer = KaldiRecognizer(model, 16000)

    print("Say something...")
    save = ""  
    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    
    while True:
        object_feature = True  # For opting out of normal detection in case of environment feature
        try:
            data = stream.read(4000)
        except OSError:  # Open new audio stream when it was closed
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
            data = stream.read(4000)
            save = ""              

        if len(data) == 0:
            break

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            data = json.loads(result)
            if "text" in data:
                if data["text"] == "":  # Reset log once stops talking (delete previous commands)
                    save = ""

                # Add text recognized to log
                save += " " + data["text"]
                print(save)

                nouns = find_command(save)
                subject_count = 0

                if nouns is not None:
                    for noun in nouns:  # Environment feature path
                        if noun == "environment" or noun == "environments":  # Add more similar sounding words
                            subject_count += 1
                            object_feature = False
                            close_stream(stream, p)
                            detect(yolo, vid, noun)
                            speak("Completed.")

                    if object_feature:  # Normal path
                        for noun in nouns:  # Make sure only one subject, if more count
                            if noun in classes:
                                subject_count += 1
                                print(noun + " was added to subject_count")
                            else:  # Noun is not in a class
                                print(noun + " is not a detectable class")
                                speak(noun + " is not a detectable class")

                        if subject_count > 1:
                            print("You have called for multiple objects: ")
                            speak("You have called for multiple objects: ")
                            for noun in nouns:
                                print(noun + " ")
                                speak(noun + " ")
                            print("Which object are you looking for? Repeat your command.")
                            speak("Which object are you looking for? Repeat your command.")
                        elif subject_count == 1:
                            for noun in nouns:  # Only one noun
                                print("DETECTING " + noun)
                                speak("DETECTING " + noun)
                                close_stream(stream, p)
                                detect(yolo, vid, noun)

live_speech_to_text()
