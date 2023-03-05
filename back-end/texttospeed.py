from gtts import gTTS
import os
import threading
from playsound import playsound
from time import *

def text_to_sound(text, id):
    tts = gTTS(str(id)+ text,tld='com.vn',lang='vi')
    tts.save("sound/sound.mp3")    
    playsound("sound/sound.mp3",True)


def start_sound(text, id):
    thread = threading.Thread(target=text_to_sound, args=(text,id,))
    thread.start()
    while True:
        try:
            os.remove("sound/sound.mp3")
        except:
            break