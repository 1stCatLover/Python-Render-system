import pygame
import random
def gradient(*args, start = 'top'):
    pts = []
    for a in args:
        if isinstance(a, (tuple, list)):
            pts.append(a)
    return CreateGradientStrict(*pts,align=start)

def rgb(r,g,b):
    return (r,g,b)

def CreateGradientStrict(*colors, detailLevel=50, align="top"):
    colorss = colors
    steps = len(colors) * detailLevel 

    #size
    if align in ["top-left", "top-right", "bottom-left", "bottom-right", "center"]:
        width = height = steps  # square for diagonal or center
    elif align in ["left", "right"]:
        width, height = steps, 1  # horizontal gradient
    else:
        width, height = 1, steps  # vertical gradient

    # create surface
    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # gradient TIME
    if align == "center":
        # center expands outward
        for y in range(height):
            for x in range(width):
                dx = abs(x - width // 2) / (width // 2)
                dy = abs(y - height // 2) / (height // 2)
                t = max(dx, dy)
                segment = t * (len(colors) - 1)
                idx = int(segment)
                blend = segment - idx
                if idx >= len(colors) - 1:
                    c1, c2 = colors[-2], colors[-1]
                else:
                    c1, c2 = colors[idx], colors[idx + 1]
                r = int(c1[0] + (c2[0] - c1[0]) * blend)
                g = int(c1[1] + (c2[1] - c1[1]) * blend)
                b = int(c1[2] + (c2[2] - c1[2]) * blend)
                surf.set_at((x, y), (r, g, b))

    elif align in ["top-left", "top-right", "bottom-left", "bottom-right"]:
        # diagonal gradient
        for y in range(height):
            for x in range(width):
                # diagonal progress
                if align == "top-left":
                    t = (x + y) / (width + height - 2)
                elif align == "top-right":
                    t = ((width - 1 - x) + y) / (width + height - 2)
                elif align == "bottom-left":
                    t = (x + (height - 1 - y)) / (width + height - 2)
                elif align == "bottom-right":
                    t = ((width - 1 - x) + (height - 1 - y)) / (width + height - 2)

                segment = t * (len(colors) - 1)
                idx = int(segment)
                blend = segment - idx
                if idx >= len(colors) - 1:
                    c1, c2 = colors[-2], colors[-1]
                else:
                    c1, c2 = colors[idx], colors[idx + 1]
                r = int(c1[0] + (c2[0] - c1[0]) * blend)
                g = int(c1[1] + (c2[1] - c1[1]) * blend)
                b = int(c1[2] + (c2[2] - c1[2]) * blend)
                surf.set_at((x, y), (r, g, b))

    elif align in ["left", "right"]:
        # horizontal gradient
        for x in range(width):
            t = x / (width - 1)
            if align == "right":
                t = 1 - t  # flip for right
            segment = t * (len(colors) - 1)
            idx = int(segment)
            blend = segment - idx
            if idx >= len(colors) - 1:
                c1, c2 = colors[-2], colors[-1]
            else:
                c1, c2 = colors[idx], colors[idx + 1]
            r = int(c1[0] + (c2[0] - c1[0]) * blend)
            g = int(c1[1] + (c2[1] - c1[1]) * blend)
            b = int(c1[2] + (c2[2] - c1[2]) * blend)
            surf.set_at((x, 0), (r, g, b))

    elif align in ["top", "bottom"]:
        # vertical gradient
        for y in range(height):
            t = y / (height - 1)
            if align == "bottom":
                t = 1 - t  # flip for bottom
            segment = t * (len(colors) - 1)
            idx = int(segment)
            blend = segment - idx
            if idx >= len(colors) - 1:
                c1, c2 = colors[-2], colors[-1]
            else:
                c1, c2 = colors[idx], colors[idx + 1]
            r = int(c1[0] + (c2[0] - c1[0]) * blend)
            g = int(c1[1] + (c2[1] - c1[1]) * blend)
            b = int(c1[2] + (c2[2] - c1[2]) * blend)
            surf.set_at((0, y), (r, g, b))

    return ["gradient", surf, colorss, align]


def RandomGradient(MaxColors,Detail=50,WhatWay="top"):
    count = 0
    Max = random.randint(2,MaxColors)
    Colors = []
    while count < Max:
        count += 1
        Colors.append([random.randint(1,255),random.randint(1,255),random.randint(1,255)])
    return CreateGradientStrict(Colors, Detail, WhatWay)