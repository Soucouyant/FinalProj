# Dependencies
import pygame
from sys import exit
from settings import *
from levels import *

# Game Class
# When code scales, it will be much easier to modify this class rather than a function
class Game:
    # Init
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(gameName)
        
        # Icon 
        self.Icon = pygame.image.load(iconPath)
        pygame.display.set_icon(self.Icon)
        #######################################
        
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        
        # Init Level One
        self.level = level()
    
    # Game Loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            # Game Setup
            self.screen.fill(blackRGB)
                
            # Render Level
            self.level.render()

            # Update
            pygame.display.update()
            self.clock.tick(FPS)

# Create Game OBJ and call run
game = Game()
game.run()