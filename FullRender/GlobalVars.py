import pygame
ScreenSize = (400, 400)
FPS = 240



# region You do not need to change past here...
Parts = [[],[]]
screen = pygame.display.set_mode(ScreenSize,pygame.RESIZABLE,vsync=1)
Sounds =  [] #sounds that are currently playing
PartsOri = []
CurrentFps = 0
CurrentSec = 0
CurrentMin = 0
CurrentHr = 0
UpdateFrame = False
GravObjects = [] #Object[Name,Vl[X,Y],bounce,offset]

import threading
render_lock = threading.Lock()
# endregion