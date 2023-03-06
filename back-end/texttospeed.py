from gtts import gTTS
import os
import threading
from playsound import playsound
from time import *

def text_to_sound(text, id):
    if os.path.exists("sound/sound.mp3"):
        os.remove("sound/sound.mp3")
    tts = gTTS(str(id)+ text,tld='com.vn',lang='vi')
    tts.save("sound/sound.mp3")    
    playsound("sound/sound.mp3",True)
    event = threading.Event()
    event.wait(2)


def start_sound(text, id):
    thread = threading.Thread(target=text_to_sound, args=(text,id,))
    thread.start()