import Render.GlobalVars as var
from pygame import mixer
from time import sleep
from pathlib import Path

# region Sound
Sounds = []
def Play(SoundFile,SoundName):
    global Sounds
    sound = mixer.Sound(SoundFile)
    pos = len(Sounds[0])
    Sounds[0].append(sound)
    Sounds[1].append(sound.get_length())
    Sounds[2].append(0)
    Sounds[3].append(SoundName)
    Sounds[0][pos].play()

"""
-------------------- W.I.P. --------------------

def Stop(*args):
    for i in args:
        Del = Sounds[1].index(i)
        Sounds[0].pop(Del)
        Sounds[1].pop(Del)

def MainSound():
    while True:
        print()
        sleep(1)
# endregion
"""