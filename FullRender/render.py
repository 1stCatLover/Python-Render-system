
import pygame, math, requests, io, random, inspect, threading, pathlib, time
import GlobalVars as Var
clock =  pygame.time.Clock()

class Color:
    def gradient(*args, start = 'top'):
        pts = []
        for a in args:
            if isinstance(a, (tuple, list)):
                pts.append(a)
        return Color.CreateGradientStrict(*pts,align=start)

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
        Colo = []
        while count < Max:
            count += 1
            Colo.append([random.randint(1,255),random.randint(1,255),random.randint(1,255)])
        return Color.CreateGradientStrict(Color, Detail, WhatWay)

class Shape:
    def Rect(
        X, Y, width, height,
        fill=(0, 0, 0),
        border=None,
        borderWidth=2,
        radius=0,
        opacity=255,
        rotateAngle=0,
        Screen=Var.screen,
        render=False
    ):
        has_border = border is not None
        bw = borderWidth if has_border else 0

        total_w = width + bw * 2
        total_h = height + bw * 2

        surf = pygame.Surface((total_w, total_h), pygame.SRCALPHA)

        outer_rect = pygame.Rect(0, 0, total_w, total_h)
        inner_rect = pygame.Rect(bw, bw, width, height)

        # Border
        if has_border:
            if isinstance(border, list) and border[0] == "gradient":
                grad = pygame.transform.smoothscale(border[1], (total_w, total_h))
                mask = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
                pygame.draw.rect(
                    mask,
                    (255, 255, 255),
                    outer_rect,
                    border_radius=radius + bw
                )
                grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                surf.blit(grad, (0, 0))
            else:
                pygame.draw.rect(
                    surf,
                    border,
                    outer_rect,
                    border_radius=radius + bw
                )

        # Fill
        if isinstance(fill, list) and fill[0] == "gradient":
            grad = pygame.transform.smoothscale(fill[1], (width, height))
            mask = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(
                mask,
                (255, 255, 255),
                mask.get_rect(),
                border_radius=radius
            )
            grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surf.blit(grad, inner_rect.topleft)
        else:
            pygame.draw.rect(
                surf,
                fill,
                inner_rect,
                border_radius=radius
            )
        if opacity < 255:
            surf.set_alpha(opacity)

        if rotateAngle:
            surf = pygame.transform.rotate(surf, rotateAngle)

        rect = surf.get_rect(topleft=(X, Y))

        if render:
            Screen.blit(surf, rect)

        return surf, rect

    def Oval(X, Y, width, height, fill=(0,0,0), border=None,
            borderWidth=2, opacity=255, rotateAngle=0,
            Screen = Var.screen, render = False):


        TempSurf = pygame.Surface((width + borderWidth*2, height + borderWidth*2), pygame.SRCALPHA)

        if border:
            if border[0] == "gradient":
                TempSurf.blit(pygame.transform.scale(border[1], (width + borderWidth*2, height + borderWidth*2)), (0,0))
            else:
                pygame.draw.ellipse(TempSurf, border, pygame.Rect(0,0,width + borderWidth*2, height + borderWidth*2))

        if fill[0] == "gradient":
            scaled_fill = pygame.transform.scale(fill[1], (width, height))
            mask = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.ellipse(mask, (255,255,255), pygame.Rect(0,0,width,height))
            scaled_fill.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            TempSurf.blit(scaled_fill, (borderWidth, borderWidth))
        else:
            pygame.draw.ellipse(TempSurf, fill, pygame.Rect(borderWidth, borderWidth, width, height))
        #transparency
        TempSurf.set_alpha(opacity)
        #rotate
        RotatedSurf = pygame.transform.rotate(TempSurf, rotateAngle)
        #pos
        RotatedRect = RotatedSurf.get_rect(topleft=(X-(width/2), Y-(height/2)))
        #display
        if render == True:
            Screen.blit(RotatedSurf, RotatedRect)
        else:
            return(RotatedSurf, RotatedRect)

    def Circle(X, Y, radius, fill=(0,0,0), border=None,
            borderWidth=2, opacity=100, rotateAngle=0,
            Screen = Var.screen, render = False):
        return Shape.Oval(X,Y,radius,radius,fill,border,borderWidth,opacity,rotateAngle, Screen=Screen, render=render)

    def Line(x1, y1, x2, y2, fill=(0,0,0), lineWidth=2, opacity=255, Screen = Var.screen, render = False):

        length = int(math.hypot(x2 - x1, y2 - y1)) or 1  # distance between
        TempSurf = pygame.Surface((length, lineWidth), pygame.SRCALPHA)  # width=line length, height=lineWidth
        # Check if fill is a gradient
        if isinstance(fill, list) and fill[0] == "gradient":
            # gradient scaled to the surface
            TempSurf.blit(pygame.transform.scale(fill[1], (length, lineWidth)), (0, 0))

            # Rotate surface
            angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            RotSurf = pygame.transform.rotate(TempSurf, angle)

            # position and rotated surface
            rect = RotSurf.get_rect(center=((x1 + x2)/2, (y1 + y2)/2))

            # Set transparency
            RotSurf.set_alpha(opacity)

            # Add to screen


        else:
            # boring line
            color = pygame.Color(fill[0], fill[1], fill[2], opacity) if isinstance(fill, tuple) else fill
            pygame.draw.line(TempSurf, color, (x1, y1), (x2, y2), lineWidth)
            RotSurf = pygame.transform.rotate(TempSurf,0)
            rect = RotSurf.get_rect()
        if render == True:
            Screen.blit(RotSurf, rect.topleft)
        else:
            return [TempSurf,rect.topleft]

    def Label(text,
                x,
                y,
                size=24,
                fill=(255, 255, 255),
                font=None,
                Screen=Var.screen,
                rotateAngle=0,
                render=False):

        global screen
        if Screen is None:
            Screen = screen

        if font is None:
            font = pygame.font.SysFont(None, size)

        pos = (x, y)

        text_surface = font.render(text, True, (255, 255, 255))
        text_w, text_h = text_surface.get_size()

        rect = pygame.Rect(x, y, text_w, text_h)

        mask_surface = pygame.Surface((text_w, text_h), pygame.SRCALPHA)
        mask_surface.blit(text_surface, (0, 0))

        is_gradient = isinstance(fill, dict) and fill.get("gradient")

        if not is_gradient:
            final_surf = font.render(text, True, fill)

        else:
            final_surf = pygame.Surface((text_w, text_h), pygame.SRCALPHA)
            final_surf.blit(fill, (0, 0))
            final_surf.blit(mask_surface, (0, 0),
                            special_flags=pygame.BLEND_RGBA_MULT)


        if rotateAngle != 0:
            final_surf = pygame.transform.rotate(final_surf, rotateAngle)
            rect = final_surf.get_rect(center=rect.center)
        if render:
            Screen.blit(final_surf, rect.topleft)
        return [final_surf, rect]

    def Polygon(*args,
                fill=(0,0,0),
                border=None,
                borderWidth=2,
                opacity=255,
                rotateAngle=0,
                Screen = Var.screen,render = False):
        points = args
        pts = [a for a in args if isinstance(a, (int, float))]
        if len(pts) % 2 != 0 or len(pts) < 6:
            return

        pointList = [(pts[i], pts[i+1]) for i in range(0, len(pts), 2)]

        xs = [p[0] for p in pointList]
        ys = [p[1] for p in pointList]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        w = max(maxx - minx, 1)
        h = max(maxy - miny, 1)

        TempSurf = pygame.Surface((w + borderWidth*2, h + borderWidth*2), pygame.SRCALPHA)
        shifted = [(x - minx + borderWidth, y - miny + borderWidth) for (x, y) in pointList]

        if isinstance(fill, list) and fill[0] == "gradient":
            grad_surf = pygame.transform.scale(fill[1], (w, h))
            mask = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.polygon(mask, (255,255,255), [(x-borderWidth, y-borderWidth) for (x,y) in shifted])
            grad_surf.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
            TempSurf.blit(grad_surf, (borderWidth, borderWidth))
        else:
            pygame.draw.polygon(TempSurf, fill, shifted)

        if border is not None:
            if isinstance(border, list) and border[0] == "gradient":
                bw, bh = w + borderWidth*2, h + borderWidth*2
                grad_surf = pygame.transform.scale(border[1], (bw, bh))
                mask = pygame.Surface((bw, bh), pygame.SRCALPHA)
                pygame.draw.polygon(mask, (255,255,255), shifted)
                grad_surf.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
                TempSurf.blit(grad_surf, (0,0))
            else:
                pygame.draw.polygon(TempSurf, border, shifted, borderWidth)

        # --- FINALIZE ---
        TempSurf.set_alpha(opacity)
        if rotateAngle != 0:
            TempSurf = pygame.transform.rotate(TempSurf, rotateAngle)

        rect = TempSurf.get_rect(topleft=(minx - borderWidth, miny - borderWidth))
        if render == True:
            Screen.blit(TempSurf, rect)
        else:
            return(TempSurf,rect)

    def Image(X, Y, file_path,
                width=None, height=None,
                opacity=255, rotateAngle=0,
                Screen=Var.screen, render=False):

        try:
            TempSurf = pygame.image.load(file_path).convert_alpha()
        except Exception as e:
            print(f"Failed to load image '{file_path}': {e}")
            return

        if width is not None and height is not None:
            TempSurf = pygame.transform.scale(TempSurf, (width, height))
        elif width is not None:  # preserve aspect ratio
            ratio = width / TempSurf.get_width()
            height = int(TempSurf.get_height() * ratio)
            TempSurf = pygame.transform.scale(TempSurf, (width, height))
        elif height is not None:
            ratio = height / TempSurf.get_height()
            width = int(TempSurf.get_width() * ratio)
            TempSurf = pygame.transform.scale(TempSurf, (width, height))

        TempSurf.set_alpha(opacity)

        if rotateAngle != 0:
            TempSurf = pygame.transform.rotate(TempSurf, rotateAngle)

        RotatedRect = TempSurf.get_rect(topleft=(X, Y))

        if render:
            Screen.blit(TempSurf, RotatedRect)
        else:
            return (TempSurf, RotatedRect)

    def URLImage(X, Y, url,
                    width=None, height=None,
                    opacity=255, rotateAngle=0,
                    Screen=Var.screen, render=False):

        # Fetch image from URL
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_file = io.BytesIO(response.content)
            TempSurf = pygame.image.load(image_file).convert_alpha()
        except Exception as e:
            print(f"Failed to load image from URL '{url}': {e}")
            return

        if width is not None and height is not None:
            TempSurf = pygame.transform.scale(TempSurf, (width, height))
        elif width is not None:
            ratio = width / TempSurf.get_width()
            height = int(TempSurf.get_height() * ratio)
            TempSurf = pygame.transform.scale(TempSurf, (width, height))
        elif height is not None:
            ratio = height / TempSurf.get_height()
            width = int(TempSurf.get_width() * ratio)
            TempSurf = pygame.transform.scale(TempSurf, (width, height))

        TempSurf.set_alpha(opacity)

        if rotateAngle != 0:
            TempSurf = pygame.transform.rotate(TempSurf, rotateAngle)

        RotatedRect = TempSurf.get_rect(topleft=(X, Y))

        if render:
            Screen.blit(TempSurf, RotatedRect)
        else:
            return (TempSurf, RotatedRect)
        
class Util:
    def timer_thread():
        clock = pygame.time.Clock()
        while True:
            Var.CurrentFps += 1
            if Var.CurrentFps >= Var.FPS:
                Var.CurrentFps = 0
                Var.CurrentSec += 1
            if Var.CurrentSec >= 60:
                Var.CurrentSec = 0
                Var.CurrentMin += 1
            if Var.CurrentMin >= 60:
                Var.CurrentMin = 0
                Var.CurrentHr += 1
            clock.tick(Var.FPS)
            #print(var.CurrentFps,var.CurrentSec,var.CurrentMin,var.CurrentHr)

    def MoveSurf(Object, X,Y):
        return [Object,Object.get_rect(topleft=(X, Y))]

    def GetPos(Name):
        if isinstance(Name,list):
            for name in Name:
                X=Var.Parts[0][Var.Parts[1].index(name)][1].x
                Y=Var.Parts[0][Var.Parts[1].index(name)][1].y
        else:
            X=Var.Parts[0][Var.Parts[1].index(Name)][1].x
            Y=Var.Parts[0][Var.Parts[1].index(Name)][1].y
        return [X,Y]
    def GetSize(Name):
        if isinstance(Name,list):
            for name in Name:
                Size=Var.Parts[0][Var.Parts[1].index(name)][0].get_size()
        else:
            Size=Var.Parts[0][Var.Parts[1].index(Name)][0].get_size()
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
        t = threading.Thread(target=Util.timer_thread, daemon=True)
        t.start()
        t = threading.Thread(target=Music, daemon=True)
        t.start()

class Scene:
    def AddObject(*args): #input object then name so [rect(args), "rectangle"]
        for i in args:
            Var.Parts[0].append(i[0])
            Var.Parts[1].append(i[1])
        Var.UpdateFrame = True

    def RemoveObject(*args):
        for i in args:

            if i in Var.Parts[1]:
                idx = Var.Parts[1].index(i)

                Var.Parts[0].pop(idx)
                Var.Parts[1].pop(idx)

        Var.UpdateFrame = True

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
        Var.UpdateFrame = True
        if isinstance(Name,list):
            for name in Name:
                Var.Parts[0][Var.Parts[1].index(name)][1].move_ip(pos)
        else:
            Var.Parts[0][Var.Parts[1].index(Name)][1].move_ip(pos)

    # endregion


    # region working on
    def grav():
        while True:
            for Object in Var.GravObjects:
                size = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
                OffsetX = -200
                OffsetY = -200
                PaSizeX = Object[3][0]
                PaSizeY = Object[3][1]
                Object[1][1] += .3
                pos = Util.GetPos(Object[0])
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


                Scene.Move(Object[0],Object[1])
            clock.tick(80)

    def ObjectGravity(Object,Bounce):
        a=a
    # endregion

class Music:
    Fade = 2
    CurrentPlaylist = []
    def Randomise(Playlist = None):
        if Playlist == None:
            MusicToAdd = CurrentPlaylist
            MusicOrderNew = []
            for i in range(0,len(CurrentPlaylist)):
                rand = random.randint(0,len(MusicToAdd)-1)
                MusicOrderNew.append(MusicToAdd[rand])
                MusicToAdd.pop(rand)
            CurrentPlaylist = MusicOrderNew
    def Add(*musics,Random=False):
        for item in musics:
            path = pathlib.Path(item)

            if path.is_dir():
                for file in path.iterdir():
                    if file.is_file():
                        Music.CurrentPlaylist.append(str(file))

            elif path.is_file():
                Music.CurrentPlaylist.append(str(path))
        if Random == True:
            Music.Randomise()
        print("music",Music.CurrentPlaylist)

    def Remove(*args):
        for i in args:
            Music.CurrentPlaylist.index(i)
    def RemoveAll():
            CurrentPlaylist = []

    def Music():
        pos = -1
        while True:
            TrueFade = Music.Fade*1000
            if len(Music.CurrentPlaylist) == 0:
                time.sleep(.1)
            else:
                if pos >= len(Music.CurrentPlaylist)-1:
                    pos = 0
                else:
                    pos += 1
                pygame.mixer.music.load(Music.CurrentPlaylist[pos])
                pygame.mixer.music.play(loops=0, start=0.0, fade_ms = TrueFade)
                song = Music.CurrentPlaylist[pos]
                sound = pygame.mixer.Sound(song)
                length = sound.get_length()
                print(length)
                time.sleep(length-Music.Fade)


    # endregion

class Playlist:
    Playlists = [[],[]] # this will store [playlist,Name] playlist is just an array of sound files

    def Load(Playlist, Random = False):
        Playlist = Playlist.Playlists[1].index(Playlist)
        Music.Add(*Playlist.Playlists[0][Playlist], Random = Random)


    def Add(*Song, Name = None):
        if Name == None:
            print("Error no name for playlist")
        else:
            Playlist.Playlists[0].append([])
            Playlist.Playlists[1].append(Name)
            PlaylistSpot = Playlist.Playlists[1].index(Name)
            for Song in Song:
                Playlist.Playlists[0][PlaylistSpot].append(Song)

    def Remove(*args):
        for i in args:
            Del = Playlist.Playlists[1].index(i)
            #list.remove(Var) deletes the item that is called Var from list
            #list.pop(numb) removes the list[numb] from the list and if no number givven removes the last value
            Playlist.Playlists[0].pop(Del)
            Playlist.Playlists[1].pop(Del)

    def AddFolder(*Folder, Name = None):
        if Name == None:
            print("Error no name for playlist")
        else:
            songs = []
            for Folders in Folder:
                path = pathlib.Path(Folders)
                if path.is_dir():
                    for file in path.iterdir():
                        if file.is_file():
                            songs.append(str(file))
        Playlist.Add(*songs,Name=Name)

    def RemoveFolder(*Folder, Name = None):
        if Name == None:
            print("Error no name for playlist")
        else:
            songs = []
            for Folders in Folder:
                path = pathlib.Path(Folders)
                if path.is_dir():
                    for file in path.iterdir():
                        if file.is_file():
                            songs.remove(str(file))

    def AddSong(*Song,Playlist = None):
        Playlist = Playlist.Playlists[1].index(Playlist)
        for song in Song:
            Playlist.Playlists[0][Playlist].append(song)

    def RemoveSong(*Song,Playlist = None):
        if Playlist == None:
            print("No plalist removed")
        else:
            PlaylistNumb = Playlist.Playlists[1].index(Playlist)
            for song in Song:
                Playlist.Playlists[0][PlaylistNumb].index(song)