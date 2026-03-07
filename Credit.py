import threading, pygame, requests, io, webbrowser
from Scripts import Shape, Scene
import Render.GlobalVars as Vars

CurrentLableNumb = 0
_image_cache = {}
_cache_lock = threading.Lock()
_clickable_images = []

def preload_images(lines):
    for line in lines:
        line = line.strip()
        if line.startswith('"') and line.endswith('"'):
            continue
        if "|||" not in line:
            continue
        parts = line.split("|||")
        img_url = parts[1].strip()
        with _cache_lock:
            if img_url in _image_cache:
                continue
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            image_file = io.BytesIO(response.content)
            surf = pygame.image.load(image_file).convert_alpha()
            with _cache_lock:
                _image_cache[img_url] = surf
        except Exception as e:
            print(f"Failed to preload image '{img_url}': {e}")

Lines = []
with open("Credit.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            Lines.append(line)

threading.Thread(target=preload_images, args=(Lines,), daemon=True).start()

box_width = 0
box_height = 0
temp_surf = pygame.Surface((200, 200))
temp_surf.set_alpha(128)
box_surf, box_rect = Shape.Rect(
    X=0,
    Y=0,
    width=box_width,
    height=box_height,
    fill=(0, 0, 0, 0)
)
TotalHight = 0
_background_color = (0, 0, 0)

def Run(x=5, y=5, line_spacing=18, font_size=31, fill=(255, 255, 255),
        border_color=(255, 255, 255), border_width=3, padding=10,
        image_size=40, opacity=255, rotateAngle=0, Screen=Shape.screen,
        background=(0, 0, 0)):
    global box_height, box_width, temp_surf, box_surf, box_rect
    global CurrentLableNumb, _clickable_images, TotalHight, _background_color

    _background_color = background
    _clickable_images = []
    TotalHight = 0
    labels = []
    images = []
    max_width = Vars.ScreenSize[0] - (x * 2) - (border_width * 2)
    total_height = Vars.ScreenSize[1] - (y * 2) - (border_width * 2)

    for line in Lines:
        if line.startswith('"') and line.endswith('"'):
            display_text = line.strip('"')
            label_surface, label_rect = Shape.Label(
                text=display_text,
                x=0,
                y=0,
                size=font_size,
                fill=fill,
                render=False,
                Screen=Screen
            )
            labels.append((label_surface, label_rect))
            images.append(None)
            continue

        if "|||" not in line or "-" not in line:
            continue

        name_part, img_part = line.split("|||")
        creator_name, creator_url = name_part.split("-", 1)
        creator_name = creator_name.strip()
        creator_url = creator_url.strip()
        img_url = img_part.strip()

        img_surface_rect = None
        if img_url:
            with _cache_lock:
                surf = _image_cache.get(img_url)
            if surf:
                surf_scaled = pygame.transform.scale(surf, (image_size, image_size))
                surf_scaled.set_alpha(opacity)
                if rotateAngle != 0:
                    surf_scaled = pygame.transform.rotate(surf_scaled, rotateAngle)
                img_surface_rect = (surf_scaled, surf_scaled.get_rect(), creator_url)
                TotalHight += image_size - font_size / 2

        label_surface, label_rect = Shape.Label(
            text=creator_name,
            x=0,
            y=0,
            size=font_size,
            fill=fill,
            render=False,
            Screen=Screen
        )

        labels.append((label_surface, label_rect))
        images.append(img_surface_rect)
        TotalHight += font_size * 3.5 + line_spacing

    box_width = max_width
    box_height = total_height

    box_surf, box_rect = Shape.Rect(
        X=x,
        Y=y,
        width=box_width,
        height=box_height,
        fill=(0, 0, 0, 0),
        border=border_color,
        borderWidth=border_width,
        render=False,
        Screen=Screen
    )

    temp_surf = pygame.Surface((box_width, TotalHight), pygame.SRCALPHA)

    current_y = padding
    for (label_surface, label_rect), img_surface_rect in zip(labels, images):
        pos_x = padding
        pos_y = current_y

        if img_surface_rect:
            img_surf, img_rect, url = img_surface_rect
            img_rect.topleft = (pos_x, pos_y)
            temp_surf.blit(img_surf, img_rect)
            pos_x += image_size + 5
            _clickable_images.append((pygame.Rect(x + img_rect.left, y + img_rect.top, image_size, image_size), url))

        temp_surf.blit(label_surface, (pos_x, pos_y))
        current_y += max(label_rect.height, image_size if img_surface_rect else 0) + line_spacing

    temp_surf2 = pygame.Surface(box_surf.get_size(), pygame.SRCALPHA)
    temp_surf2.fill(background)
    temp_surf2.blit(box_surf, (0, 0))
    temp_surf2.blit(temp_surf, (0, 0))

    CurrentLableNumb += 1
    obj_name = "CreditsBox"
    Scene.AddObject([[temp_surf2, box_rect], obj_name])

    return [obj_name]


def HandleClicks(mouse_pos):
    for rect, url in _clickable_images:
        if rect.collidepoint(mouse_pos) and url:
            webbrowser.open(url)


YPos = 0

def HandleScroll(Event):
    global YPos
    YPos += Event.y * 5
    if YPos > 0:
        YPos = 0
    MaxSize = (TotalHight - Vars.ScreenSize[1]) * -1
    print(MaxSize)
    print(YPos)
    if YPos < MaxSize:
        YPos = MaxSize

    temp_surf2 = pygame.Surface(box_surf.get_size(), pygame.SRCALPHA)
    temp_surf2.fill(_background_color)
    temp_surf2.blit(box_surf, (0, 0))
    temp_surf2.blit(temp_surf, (0, YPos))

    Scene.RemoveObject("CreditsBox")
    obj_name = "CreditsBox"
    Scene.AddObject([[temp_surf2, box_rect], obj_name])
    print(Event)