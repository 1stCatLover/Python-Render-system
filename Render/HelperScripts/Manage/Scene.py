import pygame, threading, time
from Render.HelperScripts.Color import *
import Render.GlobalVars as var
from Render.HelperScripts.Util import GetPos
clock =  pygame.time.Clock()

#manage objects

# region Manageing objects

def AddObject(*args): #input object then name so [rect(args), "rectangle"]
    for i in args:
        var.Parts[0].append(i[0])
        var.Parts[1].append(i[1])
    var.UpdateFrame = True

def RemoveObject(*args):
    for i in args:

        if i in var.Parts[1]:
            idx = var.Parts[1].index(i)

            var.Parts[0].pop(idx)
            var.Parts[1].pop(idx)

    var.UpdateFrame = True


def Group(*Draw):
    pairs = []

    # Handle parallel-lists structure (Surface,Name)
    if len(Draw) == 2 and all(isinstance(x, list) for x in Draw):
        objects_list, names_list = Draw
        for obj in objects_list:
            # un wrap one level if obj is [[Surface, Rect]] (Fixes some errors)
            if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], list):
                pairs.append(tuple(obj[0]))
            else:
                pairs.append(tuple(obj))

    else:
        for item in Draw:
            if isinstance(item, tuple) and len(item) == 2:
                pairs.append(item)
            elif isinstance(item, list):
                for sub in item:
                    if isinstance(sub, tuple) and len(sub) == 2:
                        pairs.append(sub)

    if not pairs:
        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        return surf, surf.get_rect(topleft=(0, 0))

    rects = [r for _, r in pairs]

    left   = min(r.left for r in rects)
    top    = min(r.top for r in rects)
    right  = max(r.right for r in rects)
    bottom = max(r.bottom for r in rects)

    width  = right - left
    height = bottom - top

    temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for surf, rect in pairs:
        temp_surface.blit(surf, rect.move(-left, -top))

    return temp_surface, temp_surface.get_rect(topleft=(left, top))

#movement
def Move(Name,pos):
    #print(Name,pos)
    if not (isinstance(pos, tuple)):
        pos = tuple(pos)
    var.UpdateFrame = True
    if isinstance(Name,list):
        for name in Name:
            var.Parts[0][var.Parts[1].index(name)][1].move_ip(pos)
    else:
        var.Parts[0][var.Parts[1].index(Name)][1].move_ip(pos)

# endregion


# region working on
def grav():
    while True:
        for Object in var.GravObjects:
            size = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
            OffsetX = -200
            OffsetY = -200
            PaSizeX = Object[3][0]
            PaSizeY = Object[3][1]
            Object[1][1] += .3
            pos = GetPos(Object[0])
            if pos[0] >= size[0]+OffsetX-PaSizeX:
                Object[1][0] = -abs(Object[1][0])

            if pos[0] <= 0+OffsetX+PaSizeX:
                Object[1][0] = abs(Object[1][0])
            if pos[1] >= size [1]+OffsetY-PaSizeY:
                Object[1][1] = -abs(Object[1][1])
                Object[1][1] =+ (Object[1][1]*Object[2])
                if Object[1][1] >= 1:
                    Object[1][1] = 0
            if pos[1] <= 0+OffsetY+PaSizeY:
                Object[1][1] = abs(Object[1][1])

            
            Move(Object[0],Object[1])
        clock.tick(80)
    
def ObjectGravity(Object,Bounce):
    a=a
# endregion
