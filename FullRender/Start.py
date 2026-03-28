
from render import Scene, Color, Shape, Util
import Credit as Credits
from time import sleep
import pygame, threading
import GlobalVars as var
clock = pygame.time.Clock()

Group,rgb,gradient = Scene.Group, Color.rgb, Color.gradient
Rect,Polygon,Oval,Circle = Shape.Rect, Shape.Polygon, Shape.Oval, Shape.Circle
###starting scene 
#background
# ALLL OF THIS IS NOT MINE I AM USING A FRIENDS IMAGE THANK YOU PARKER

credets = Shape.Label("Credits",290,340,50,(255,255,255),rotateAngle=45)
DisplayCredits = False
cred = []
def Event(event):
    global DisplayCredits
    global cred
    if event.type == pygame.KEYUP:
        print(pygame.K_e)
        if event.key == pygame.K_e:
            print("K")
        print(event)
        print(event.key)
    if DisplayCredits:
        if event.type == pygame.MOUSEBUTTONUP:
            Credits.HandleClicks(event.pos)
    if event.type == pygame.MOUSEWHEEL:
        Credits.HandleScroll(event)
    elif event.type == pygame.MOUSEBUTTONUP:
        if credets[1].collidepoint(event.pos):
            if DisplayCredits == False:
                DisplayCredits = True
                cred = (Credits.Run())
            else:
                print(len(cred))
                for i in range(0,len(cred)):
                    print(cred[0])
                    DisplayCredits = False
                    Scene.RemoveObject(cred[0])
                    cred.pop(0)

def an1():
    for i in range(1,120):
       Scene.Move('background',(0,-1))
       Scene.Move('shop',(0,-4))
       clock.tick(60)
def an2():
    for i in range(1,75):
       Scene.Move('sun',(0,-1))
       clock.tick(50)
def an3():
    for i in range(1,95):
       Scene.Move('tree',(2,-1))
       clock.tick(58)
def animate():
    sleep(.1)
    Scene.Move('shop',(0,480))
    sleep(1)
    print("GO")
    t = threading.Thread(target=an1, daemon=True)
    t.start()
    t = threading.Thread(target=an2, daemon=True)
    t.start()
    t = threading.Thread(target=an3, daemon=True)
    t.start()
    for i in range(1,120):
       clock.tick(60)
    print(2)
    Scene.RemoveObject('sun')
    #DELETS THE SUN
    var.UpdateFrame = True
def Start():
    credits = Shape.Label("Credits",290,340,50,(255,255,255),rotateAngle=45)
    #ball = Group(Circle(200, 220, 80, fill=gradient(rgb(255, 255, 255), rgb(255, 255, 255), rgb(255, 255, 100),start="center"), opacity=100),)
    sky = Rect(0, 0, 400, 250, fill=gradient(rgb(255, 69, 0), rgb(255, 165, 0), rgb(255, 160, 122), rgb(255, 105, 180), rgb(150, 0, 150), start='bottom'))
    sun = Group(
        Circle(200, 220, 80, fill=gradient(rgb(255, 255, 255), rgb(255, 255, 255), rgb(255, 255, 100),start="center"), opacity=225),
    )
    background = Group(
        Rect(0, 250, 400, 150, fill=gradient(rgb(255, 40, 0), rgb(255, 165, 0), start='top')),
        Polygon(0, 300, 400, 330, 400, 550, 0, 550, fill=gradient(rgb(120, 20, 0), rgb(255, 70, 0), start='bottom')),
        #left clouds
        Oval(100, 235, 200, 20, fill=gradient(rgb(255, 90, 0), rgb(255, 10, 0), rgb(220, 0, 0), start='left')),
        Oval(70, 70, 200, 100, fill=gradient(rgb(150, 0, 150), rgb(150, 0, 150), rgb(255, 135, 180), rgb(255, 160, 122), start='top')),
        Oval(250, 200, 70, 30, fill=gradient(rgb(255, 10, 0), rgb(255, 100, 0), start='left')),
        Oval(270, 100, 100, 60, fill=gradient(rgb(250, 165, 140), rgb(255, 127, 80), start='top')),
        Oval(370, 125, 200, 70, fill=gradient(rgb(255, 160, 122), rgb(255, 127, 80), rgb(255, 165, 0), start='top')),
        Oval(300, 50, 400, 100, fill=gradient(rgb(150, 0, 150), rgb(150, 0, 150), rgb(255, 135, 180), rgb(255, 160, 122), start='top')),
    )

    tree = Group(
        Polygon(-20, 350, 20, 350, 150, 150, 170, 100, 135, 150, fill=gradient(rgb(227, 60, 0), rgb(180, 50, 0), rgb(50, 0, 0), start='bottom')),
        Polygon(170, 100, 150, 150, 170, 230, 180, 150, fill=gradient(rgb(100, 100, 70), rgb(180, 50, 0), start='top')),
        Polygon(170, 100, 190, 140, 230, 180, 220, 130, fill=gradient(rgb(100, 100, 70), rgb(180, 50, 0), start='top')),
        Polygon(170, 100, 140, 150, 70, 210, 105, 140, fill=gradient(rgb(100, 100, 70), rgb(180, 50, 0), start='top')),
        Polygon(170, 100, 105, 130, 60, 130, 105, 100, fill=gradient(rgb(100, 100, 70), rgb(120, 80, 40), rgb(180, 50, 0), start='right-top')),
    )
    shop = Group(
    #inside
    Rect(100, 100, 180, 100, fill=rgb(50, 30, 0)),
    Rect(105, 150, 170, 120, fill=gradient(rgb(100, 50, 0), rgb(250, 120, 0), start='left-bottom')),
        #utilities
    Rect(105, 105, 60, 40, fill=gradient(rgb(170, 170, 170), rgb(100, 100, 100), start='top')),
    Rect(110, 115, 50, 25, fill=gradient(rgb(119, 136, 153), rgb(119, 160, 180), start='left-bottom')),
    #Line(135, 115, 140, 140, fill=rgb(119, 170, 190)),
    #Line(145, 115, 150, 140, fill=rgb(119, 170, 190)),
    Rect(205, 105, 80, 40, fill=gradient(rgb(160, 160, 160), rgb(240, 240, 240), start='left-bottom')),
    #Line(215, 115, 215, 105, fill=rgb(130, 130, 130)),
    #chef,
    #front borders
    Polygon(25, 275, 25, 215, 45, 195, 355, 195, 350, 100, 380, 45, 380, 230, 335, 275, fill=rgb(50, 30, 0)),
    Rect(25, 95, 80, 130, fill=rgb(50, 30, 0)),
    Rect(275, 95, 80, 130, fill=rgb(50, 30, 0)),
    
    #shop
    Rect(30, 220, 300, 50, fill=gradient(rgb(100, 50, 0), rgb(200, 80, 0), start='bottom')),
    Polygon(30, 220, 330, 220, 350, 200, 50, 200, fill=gradient(rgb(210, 80, 0), rgb(250, 120, 0), start='bottom')),
    Polygon(330, 270, 330, 100, 375, 50, 375, 225, fill=gradient(rgb(100, 50, 0), rgb(200, 80, 0), rgb(220, 100, 0), rgb(255, 160, 0), start='bottom')),
    Rect(30, 100, 50, 120, fill=gradient(rgb(200, 80, 0), rgb(250, 120, 0), start='bottom')),
    Polygon(80, 100, 80, 220, 100, 200, 100, 100, fill=gradient(rgb(200, 80, 0), rgb(255, 160, 0), start='bottom')),
    Rect(280, 100, 50, 120, fill=gradient(rgb(200, 80, 0), rgb(250, 120, 0), start='bottom')),
    #top
    Polygon(10, 105, 35, 45, 380, 45, 355, 105, fill=rgb(50, 30, 0)),
    Polygon(20, 100, 65, 100, 85, 50, 40, 50, fill=rgb(140, 0, 0)),
    Polygon(65, 100, 105, 100, 125, 50, 85, 50, fill=rgb(255, 255, 230)),
    Polygon(105, 100, 145, 100, 165, 50, 125, 50, fill=rgb(140, 0, 0)),
    Polygon(145, 100, 185, 100, 205, 50, 165, 50, fill=rgb(255, 255, 230)),
    Polygon(185, 100, 225, 100, 245, 50, 205, 50, fill=rgb(140, 0, 0)),
    Polygon(225, 100, 265, 100, 285, 50, 245, 50, fill=rgb(255, 255, 230)),
    Polygon(265, 100, 305, 100, 325, 50, 285, 50, fill=rgb(140, 0, 0)),
    Polygon(305, 100, 350, 100, 370, 50, 325, 50, fill=rgb(255, 255, 230)),
    #plates
    Oval(130, 205, 50, 30, fill=rgb(50, 30, 0)),
    Oval(130, 205, 40, 20, fill=rgb(255, 255, 230)),
    Oval(130, 204, 25, 10, fill=(255,255,255), border=rgb(220, 220, 220)),
    Oval(190, 205, 50, 30, fill=rgb(50, 30, 0)),
    Oval(190, 205, 40, 20, fill=rgb(255, 255, 230)),
    Oval(190, 204, 25, 10, fill=(255,255,255), border=rgb(220, 220, 220)),
    Oval(250, 205, 50, 30, fill=rgb(50, 30, 0)),
    Oval(250, 205, 40, 20, fill=rgb(255, 255, 230)),
    Oval(250, 204, 25, 10, fill=(255,255,255), border=rgb(220, 220, 220)),
    #pathway
    Oval(45, 305, 50, 30, fill=rgb(50, 30, 0)),
    Oval(120, 320, 50, 30, fill=rgb(50, 30, 0)),
    Oval(195, 305, 50, 30, fill=rgb(50, 30, 0)),
    Oval(270, 320, 50, 30, fill=rgb(50, 30, 0)),
    Oval(345, 305, 50, 30, fill=rgb(50, 30, 0)),
    )
    threading.Thread(target=animate, daemon=True).start()
    
    var.Parts = Util.with_names(sky,sun,background,tree,shop,credits)