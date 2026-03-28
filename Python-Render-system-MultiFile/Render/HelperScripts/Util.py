import inspect, pygame
import Render.GlobalVars as var
import threading



def timer_thread():
    clock = pygame.time.Clock()
    while True:
        var.CurrentFps += 1
        if var.CurrentFps >= var.FPS:
            var.CurrentFps = 0
            var.CurrentSec += 1
        if var.CurrentSec >= 60:
            var.CurrentSec = 0
            var.CurrentMin += 1
        if var.CurrentMin >= 60:
            var.CurrentMin = 0
            var.CurrentHr += 1
        clock.tick(var.FPS)
        #print(var.CurrentFps,var.CurrentSec,var.CurrentMin,var.CurrentHr)

def MoveSurf(Object, X,Y):
    return [Object,Object.get_rect(topleft=(X, Y))]

def GetPos(Name):
    if isinstance(Name,list):
        for name in Name:
            X=var.Parts[0][var.Parts[1].index(name)][1].x
            Y=var.Parts[0][var.Parts[1].index(name)][1].y
    else:
        X=var.Parts[0][var.Parts[1].index(Name)][1].x
        Y=var.Parts[0][var.Parts[1].index(Name)][1].y
    return [X,Y]
def GetSize(Name):
    if isinstance(Name,list):
        for name in Name:
            Size=var.Parts[0][var.Parts[1].index(name)][0].get_size()
    else:
        Size=var.Parts[0][var.Parts[1].index(Name)][0].get_size()
    return Size
def with_names(*items):
    frame = inspect.currentframe().f_back
    local_vars = frame.f_locals

    names = []
    for item in items:
        #Find var name
        for var_name, var_value in local_vars.items():
            if var_value is item:
                names.append(var_name)
                break

    return [list(items), names]
def Start():
    t = threading.Thread(target=timer_thread, daemon=True)
    t.start()
    from Render.HelperScripts.Manage.Sound.Music import Music
    t = threading.Thread(target=Music, daemon=True)
    t.start()
