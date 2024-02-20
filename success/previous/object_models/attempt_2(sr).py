
 # for some reason doesn't work
#           test in quiet room, perhaps remove ambient noise adjustment
#
#
#
#       NOT LIVE 
#
#



import speech_recognition as sr

r = sr.Recognizer()

print("Start speaking...")

with sr.Microphone() as source:
    print('Microphone initialized...')
    r.adjust_for_ambient_noise(source)  # Adjust for ambient noise      #PERHAPS IS ISSUE
    print('Adjusting for ambient noise...')
    
    try:
        audio = r.listen(source, timeout=5)  # Set a timeout (in seconds) to avoid infinite waiting
        print('Audio captured...')
        
        text = r.recognize_google(audio, language='en-in')
        print('Speech recognized:', text)
    
    except sr.WaitTimeoutError:
        print('No speech detected within the timeout period. Exiting...')
    except sr.UnknownValueError:
        print('Speech recognition could not understand audio')
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
