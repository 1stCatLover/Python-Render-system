import Render.GlobalVars as var
from pygame import mixer
from time import sleep
from pathlib import Path
from random import randint
# region Music
Fade = 2
CurrentPlaylist = []
def Randomise(Playlist = None):
    if Playlist == None:
        MusicToAdd = CurrentPlaylist
        MusicOrderNew = []
        for i in range(0,len(CurrentPlaylist)):
            rand = randint(0,len(MusicToAdd)-1)
            MusicOrderNew.append(MusicToAdd[rand])
            MusicToAdd.pop(rand)
        CurrentPlaylist = MusicOrderNew
def Add(*musics,Random=False):
    for item in musics:
        path = Path(item)

        if path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    CurrentPlaylist.append(str(file))

        elif path.is_file():
            CurrentPlaylist.append(str(path))
    if Random == True:
        Randomise()
    print("music",CurrentPlaylist)

def Remove(*args):
    for i in args:
        CurrentPlaylist.index(i)
def RemoveAll():
        CurrentPlaylist = []

def Music():
    pos = -1
    while True:
        TrueFade = Fade*1000
        if len(CurrentPlaylist) == 0:
            sleep(.1)
        else:
            if pos >= len(CurrentPlaylist)-1:
                pos = 0
            else:
                pos += 1
            mixer.music.load(CurrentPlaylist[pos])
            mixer.music.play(loops=0, start=0.0, fade_ms = TrueFade)
            song = CurrentPlaylist[pos]
            sound = mixer.Sound(song)
            length = sound.get_length()
            print(length)
            sleep(length-Fade)


# endregion
