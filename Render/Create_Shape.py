import pygame, math, requests, io
from Render.GlobalVars import screen

def Rect(
    X, Y, width, height,
    fill=(0, 0, 0),
    border=None,
    borderWidth=2,
    radius=0,
    opacity=255,
    rotateAngle=0,
    Screen=screen,
    render=False
):
    has_border = border is not None
    bw = borderWidth if has_border else 0

    total_w = width + bw * 2
    total_h = height + bw * 2

    surf = pygame.Surface((total_w, total_h), pygame.SRCALPHA)

    outer_rect = pygame.Rect(0, 0, total_w, total_h)
    inner_rect = pygame.Rect(bw, bw, width, height)

    # Bornder
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
     Screen = screen, render = False):
    

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
       Screen = screen, render = False):
    return Oval(X,Y,radius,radius,fill,border,borderWidth,opacity,rotateAngle, Screen=Screen, render=render)

def Line(x1, y1, x2, y2, fill=(0,0,0), lineWidth=2, opacity=255, Screen = screen, render = False):
    
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
          Screen=screen,
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
            Screen = screen,render = False):
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
          Screen=screen, render=False):

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
             Screen=screen, render=False):

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
