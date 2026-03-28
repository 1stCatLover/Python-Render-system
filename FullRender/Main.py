import pygame
from pygame import mixer
from time import sleep
import GlobalVars as var
from render import Scene, Util, Music, Playlist
#Set Music quality
mixer.init() 
pygame.mixer.init(frequency=48000, size=-16, channels=1, buffer=1024)
# region Vars to not edit
var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
var.UpdateFrame = True
clock = pygame.time.Clock()
# endregion
#from Test.Blocks import Event
#from Test.Blocks import Start
def main():
    
    import Start
    
    Game = Start
    Util.Start() # starts other utility stuff such as music, and play time
    running = True
    Music.Add("Music")
    Game.Start()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.WINDOWRESIZED:
                var.ScreenSize = (pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])
                var.UpdateFrame = True
            Game.Event(event)
        if var.UpdateFrame == True:
            NextFrame = Scene.Group(*var.Parts)
            var.screen.fill((0,0,0))
            var.screen.blit(*NextFrame)
            var.UpdateFrame = False
        pygame.display.flip()
        
        clock.tick(var.FPS)  # limit FPS
        #Game.redraw()
    pygame.quit()


# ... other imports

pygame.init()
if __name__ == "__main__":

    var.Parts = [[],[]]
    pygame.init()
    main()
    