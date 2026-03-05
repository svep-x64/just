from CONSTANTS import *
from forces import *
import random
import pygame

class Unit:
    def __init__(self, x, y, width, height, texture=None, color=None):
        self.width, self.height = width, height
        self.color = color
        
        if texture:
            self.image = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(TEXTURES_DIR, "player.png")
                    ),
                (self.width, self.height)
            )
        if color:
            self.image = pygame.Surface((self.width, self.height))
            
            self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        
        self.x, self.y = x, y
        
        self.move()
    
    def move(self):
        self.rect.center = (self.x, self.y)
    
    def update(self, scr):
        self.move()
        
        scr.blit(self.image, self.rect)

class Player(Unit):
    def __init__(self):
        x, y = 200, HEIGHT / 2
        width, height = 40, 40
        
        super().__init__(x, y, width, height, texture="player.png")
        
        self.speed_y = Speed()

    def jump(self):
        self.speed_y.set_v(-JUMPFORCE)

    def update(self, scr, walls):
        super().update(scr)
        
        self.speed_y.update()        
        self.y += G * self.speed_y.get_v()
        
        return not pygame.sprite.spritecollide(self, walls, False) and self.rect.bottom > 0 and self.rect.top < HEIGHT
        

class Wall(Unit, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        color = (0, 255, 0)
        
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x, y, width, height, color=color)
        
        self.speed = speed
    
    def update(self, scr):
        super().update(scr)
        
        self.x -= self.speed
        
        if self.rect.right < 0:
            self.kill()


class WallFabric:
    def __init__(self):
        self.speed = 3
    
    def create(self):
        color = (0, 255, 0)
        
        x = WIDTH + 50
        y1, y2 = HEIGHT, 0
        
        width = 100
        height1 = random.randint(100, HEIGHT)
        
        height2 = HEIGHT - height1 // 2 - 70
        
        Wall1 = Wall(x, y1, width, height1, self.speed)
        Wall2 = Wall(x, y2, width, height2, self.speed)
        
        return Wall1, Wall2


class Score:
    def __init__(self, score):
        self.font = pygame.font.Font(None, 64)
        self.score = score
        self.text = self.font.render(str(self.score), True, (0, 0, 0))
        self.rect = self.text.get_rect(centerx=(WIDTH / 2), y=10)
    
    def update(self, scr, score):
        self.score = score
        self.text = self.font.render(str(self.score), True, (0, 0, 0))
        scr.blit(self.text, self.rect)
