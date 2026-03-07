import Render.GlobalVars as var
from Render.HelperScripts.Manage.Sound.Music import Add as MusicAdd
from pathlib import Path

Playlists = [[],[]] # this will store [playlist,Name] playlist is just an array of sound files

def Load(Playlist, Random = False):
    Playlist = Playlists[1].index(Playlist)
    MusicAdd(*Playlists[0][Playlist], Random = Random)


def Add(*Song, Name = None):
    if Name == None:
        print("Error no name for playlist")
    else:
        Playlists[0].append([])
        Playlists[1].append(Name)
        PlaylistSpot = Playlists[1].index(Name)
        for Song in Song:
            Playlists[0][PlaylistSpot].append(Song)

def Remove(*args):
    for i in args:
        Del = Playlists[1].index(i)
        #list.remove(Var) deletes the item that is called Var from list
        #list.pop(numb) removes the list[numb] from the list and if no number givven removes the last value
        Playlists[0].pop(Del)
        Playlists[1].pop(Del)

def AddFolder(*Folder, Name = None):
    if Name == None:
        print("Error no name for playlist")
    else:
        songs = []
        for Folders in Folder:
            path = Path(Folders)
            if path.is_dir():
                for file in path.iterdir():
                    if file.is_file():
                        songs.append(str(file))
    Add(*songs,Name=Name)

def RemoveFolder(*Folder, Name = None):
    if Name == None:
        print("Error no name for playlist")
    else:
        songs = []
        for Folders in Folder:
            path = Path(Folders)
            if path.is_dir():
                for file in path.iterdir():
                    if file.is_file():
                        songs.remove(str(file))

def AddSong(*Song,Playlist = None):
    Playlist = Playlists[1].index(Playlist)
    for song in Song:
        Playlists[0][Playlist].append(song)

def RemoveSong(*Song,Playlist = None):
    if Playlist == None:
        print("No plalist removed")
    else:
        PlaylistNumb = Playlists[1].index(Playlist)
        for song in Song:
            Playlists[0][PlaylistNumb].index(song)