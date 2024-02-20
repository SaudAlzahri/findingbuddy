#
#
#
#       EXTREMELY INNACURATE
#               (good, that means the mic works at least!)
# 
#


import pocketsphinx
from pocketsphinx import LiveSpeech

def live_speech_to_text():
    speech = LiveSpeech()

    print("Say something...")

    for phrase in speech:
        print('no')
        print("You said:", phrase)   

if __name__ == "__main__":
    live_speech_to_text()
