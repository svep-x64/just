import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
G = 3
FPS = 60
JUMPFORCE = 2

scr = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = True

class Speed:
    def __init__(self):
        self.v = 1
    
    def get_v(self):
        return self.v
    
    def set_v(self, v):
        self.v = v

    def update(self):
        if self.v < JUMPFORCE:
            self.v += 0.05
        if self.v > JUMPFORCE:
            self.v = JUMPFORCE

class Unit:
    def __init__(self, x, y, width, height, color):
        self.width, self.height = width, height
        self.color = color
        
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
        width, height = 50, 50
        color = (255, 255, 0)
        
        super().__init__(x, y, width, height, color)
        
        self.speed_y = Speed()

    def jump(self):
        self.speed_y.set_v(-JUMPFORCE)

    def update(self, scr):
        super().update(scr)
        
        self.speed_y.update()
        
        self.y += G * self.speed_y.get_v()
        

class Wall(Unit, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        color = (0, 255, 0)
        
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x, y, width, height, color)
        
        self.speed = 3
    
    def update(self, scr):
        super().update(scr)
        
        self.x -= self.speed
        
        if self.x < 0:
            self.kill()


class WallFabric:
    def create(self):
        color = (0, 255, 0)
        
        x = 500
        y1, y2 = HEIGHT, 0
        
        width = 100
        height1 = random.randint(100, HEIGHT)
        
        height2 = HEIGHT - height1 // 2 - 70
        
        Wall1 = Wall(x, y1, width, height1)
        Wall2 = Wall(x, y2, width, height2)
        
        return Wall1, Wall2

player = Player()
wall_fabric = WallFabric()
walls = pygame.sprite.Group()
walls.add(wall_fabric.create())

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.jump()
    
    scr.fill((0, 100, 255))
    
    player.update(scr)
    
    for wall in walls.sprites():
        wall.update(scr)
    
    clock.tick(FPS)
    pygame.display.flip()
    
pygame.quit()