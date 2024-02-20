#NOTES FOR PROFESSOR
#
#
#       this file contains the speak() function
#
#       reads out loud all results (automattically through macbook speakers)
#
#
#
#
#
#

from gtts import gTTS   #core
from playsound import playsound  #output
import os               #processor

def speak(mytext):
    # The text that you want to convert to audio 
    
    language = 'en'



    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=mytext, lang=language, slow=False) 



    # Saving the converted audio in a mp3 file
    #
    myobj.save("audio.mp3") 
    


    # Playing the converted file 
    playsound('audio.mp3')

    # removing file to avoid duplicates (for next run)
    os.remove("audio.mp3")


#speak("whatsup buddy")