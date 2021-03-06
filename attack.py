# This file controls the attack hitbox for the player
# Basically, it spawns a small transparent box in the direction that the player was facing
# The transparent box isn't visible to the end-user but it collides with the enemy, and thats how damage and collision works in the game

import pygame
from settings import *

class attack(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        
        # Get Dir
        direction = player.status.split("_")[0]
        # print(direction)
        
        # Hitbox
        self.image = pygame.image.load("data/graphics/misc/attackHitbox.png")
        
        # Spawn Box
        if direction == 'rght':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction == 'lft':
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif direction == 'dwn':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = player.rect.center)
            
            
        # self.rect = self.image.get_rect(center = player.rect.center)