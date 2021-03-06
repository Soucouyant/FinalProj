# We have different types of sprites depending on he state and direction the enemy is facing
# we import those based on a script in scripts.py that imports the entire folder as a list and returns it

# Initially I thought of using a path finding algorithim, especially since there is one native in python, however
# it didn't work as intended and kept giving me strange animation errors where the correct one wouldn't call, so I had to settle for my shoddy understanding of vector math
# Basically, I store the vector of the center of the enemys hitbox, and take the vector of the player, subract them to find the vector of the enemy to player
# I store both the distance by calculating the magnitude, as well as the direction by normalizing the vector to a unit vector and then storing it (while also accounting for null vector)

# Since we are reading animations from folder paths, I use get status to 1. find the proper status of the enemy (if its idling, running or attacking) and then making sure
# the folder paths is correct by using various string methods
# Animations are based of a var called self.status, so in the actions method I make sure that the right status is being called for the right action
# In the animate method, we find the right animation set in the animations dictionary and set the right image based off an index and the length of the animation

# There are defined cooldowns for how much an enemy can attack and get hit, we used a delta time to calculate that
# In get damage a sound is played and the amount of damage the player does is subracted from the enemies health

# in isDead we check if the enemies dead via healh and if it is kill the sprite

# There are two types of update
# in the sprite .update method, its position (movement and animations) are updated therefore it can be drawn in the group update call in levels.py

import pygame
from settings import *
from scripts import *
from entity import Entity

class Enemy(Entity):
    def __init__(self,pos,groups, invisibleSprites, damagePlayer, enemySprites):
        super().__init__(groups)
        self.spriteType = 'enemy'
        
        self.importGraphics()
        self.status = 'up'
        self.image = self.animations[self.status][self.frameIndex]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.invisibleSprites = invisibleSprites
        
        # Stats
        self.health = skeleton_data['health']
        self.attackDamage = skeleton_data['damage']
        self.speed = skeleton_data['speed']
        self.knockback = skeleton_data['knockback']
        self.attack_radius = skeleton_data['attack_radius']
        self.notice_radius = skeleton_data['notice_radius']
        
        self.canAttack = True
        self.attackTime = None
        self.attackCooldown = 400
        self.animationSpeed += 0.4
        
        self.vulnerable = True
        self.timeHit = None 
        self.invincibleDuration = 400
        
        self.damagePlayer = damagePlayer
        
        self.enemySprites = enemySprites
        
        # Sounds
        self.enemyDeath = pygame.mixer.Sound(SFX['enemy_death']['file'])
        self.enemyDeath.set_volume(SFX['enemy_death']['_vol'])
        self.enemyDamage = pygame.mixer.Sound(SFX['enemy_damage']['file'])
        self.enemyDamage.set_volume(SFX['enemy_damage']['_vol'])
        self.slashSFX = pygame.mixer.Sound(SFX['enemy_swing']['file'])
        self.slashSFX.set_volume(SFX['enemy_swing']['_vol'])
        
    def importGraphics(self):
        animPath = "data/graphics/anim_enemy/"
        self.animations = {
            
            # Run Keys
            'up': [],           # Done
            'dwn': [],          # Done   
            'lft': [],          # Done
            'rght': [],         # Done
            
            # Idle Keys
            'up_idle': [],      # Done
            'dwn_idle': [],     # Done
            'lft_idle': [],     # Done
            'rght_idle': [],    # Done
            
            # Attack Keys
            'up_attack': [],    # Done
            'dwn_attack': [],   # Done
            'lft_attack': [],   # Done
            'rght_attack': [],  # Done
            
            # Knock Back
            'impact_up': [],    # Done
            'impact_dwn': [],   # Done
            'impact_lft': [],   # Done
            'impact_rght': []   # Done
            
        }
        for animation in self.animations.keys():
            fullPath = animPath + animation
            self.animations[animation] = importFolder(fullPath)
             
    def getDirDist(self,player):
        enemyVec = pygame.math.Vector2(self.rect.center)
        playerVec = pygame.math.Vector2(player.rect.center)
        distance = (playerVec - enemyVec).magnitude()
        
        if distance > 0:
            direction = (playerVec - enemyVec).normalize()
        else:
            direction = pygame.math.Vector2()
        
        return (distance, direction)
    
    def getStatus(self, player):
        distance = self.getDirDist(player)[0]
        direction = self.getDirDist(player)[1]
        
        # Attack
        if distance <= self.attack_radius and self.canAttack:
            if not 'attack' in self.status:
                self.frameIndex = 0
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            if 'idle' in self.status:
                self.status = self.status.replace('idle', '_attack')
            if not 'attack' in self.status:
                # self.frameIndex = 0
                self.status = self.status + '_attack'
                
        # Run
        elif distance <= self.notice_radius and not 'idle' in self.status:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')
            else:
                self.status = self.status
                
        # Idling
        elif direction[0] == 0 and direction[1] == 0 and distance >= self.attack_radius and distance >= self.notice_radius:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            if not 'attack' in self.status:
                self.status = self.status + '_idle'
                
    def actions(self, player):
        if 'attack' in self.status:
            self.direction = self.getDirDist(player)[1]
            if self.direction.x > 0:
                self.status = 'rght_attack'
            elif self.direction.x < 0:
                self.status = 'lft_attack'
            
            if self.direction.y > 0:
                self.status = 'dwn_attack'
            elif self.direction.y < 0:
                self.status = 'up_attack'
            self.attackTime = pygame.time.get_ticks()
            self.damagePlayer(self.attackDamage)
            self.slashSFX.play()
            
        elif not '_attack' in self.status and not '_idle' in self.status:
            self.direction = self.getDirDist(player)[1]
            
            if self.direction.x > 0:
                self.status = 'rght'
            elif self.direction.x < 0:
                self.status = 'lft'
            
            if self.direction.y > 0:
                self.status = 'dwn'
            elif self.direction.y < 0:
                self.status = 'up'
        else:
            if self.direction.x > 0:
                self.status = 'rght'
            elif self.direction.x < 0:
                self.status = 'lft'
            
            if self.direction.y > 0:
                self.status = 'dwn'
            elif self.direction.y < 0:
                self.status = 'up'
            self.direction.x = 0
            self.direction.y = 0
        
    def animate(self):
        animation = self.animations[self.status]
        self.frameIndex += self.animationSpeed
        
        if not self.vulnerable:
            alpha = self.flicker()
            self.image.set_alpha(alpha)
            
            if self.direction.x < 0:
                animation = self.animations['impact_rght']
            elif self.direction.x > 0:
                animation = self.animations['impact_lft']
            
            if self.direction.y < 0:
                animation = self.animations['impact_dwn']
            elif self.direction.y > 0:
                animation = self.animations['impact_up']
            
            if self.frameIndex >= len(animation):
                self.frameIndex = 0
            self.image = animation[int(self.frameIndex)]
            self.rect = self.image.get_rect(center = self.hitbox.center)
        else:
            self.image.set_alpha(255)
            if self.frameIndex >= len(animation):
                if 'attack' in self.status:
                    self.canAttack = True
                self.frameIndex = 0
            self.image = animation[int(self.frameIndex)]
            self.rect = self.image.get_rect(center = self.hitbox.center)
        
    def cooldown(self):
        currentTime = pygame.time.get_ticks()
        if not self.canAttack:
            if currentTime - self.attackTime >= self.attackCooldown:
                self.canAttack = True
            
        if not self.vulnerable:
            if currentTime - self.timeHit >= self.invincibleDuration:
                self.vulnerable = True
            
    def getDamage(self,player):
        if self.vulnerable:
            self.enemyDamage.play()
            self.direction = self.getDirDist(player)[1]
            dmg = player_data['damage']
            self.health -= dmg
            
            self.timeHit = pygame.time.get_ticks()
            self.vulnerable = False
            
    def ifDead(self, player):
        if self.health <= 0:
            self.kill()
            player.kills += 1
            self.enemyDeath.play()

    def hitReaction(self):
        if not self.vulnerable:
            self.direction *= self.knockback
            
            if 'attack' in self.status:
                self.status.replace('_attack', '')

    def update(self):
        self.hitReaction()
        self.plrMove(self.speed)
        self.animate()
        self.cooldown()
 
    def enemy_update(self, player):
        self.getStatus(player)
        self.actions(player)
        self.ifDead(player)