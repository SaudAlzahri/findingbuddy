from gtts import gTTS   # Import Google Text-to-Speech
from playsound import playsound  # Import playsound for audio output
import os               

def speak(mytext):
    # Function to convert text to speech and play it

    language = 'en'  # Set the language for text-to-speech

    # Create a gTTS object with the provided text and language
    # slow=False means the speech will be at normal speed
    myobj = gTTS(text=mytext, lang=language, slow=False) 

    # Save the converted audio to a file
    myobj.save("audio.mp3") 

    # Play the saved audio file
    playsound('audio.mp3')

    # Remove the audio file after playing to avoid duplicates
    os.remove("audio.mp3")

# Example usage of the speak function
# speak("I am Finding Buddy")
