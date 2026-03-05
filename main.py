import pygame

from CONSTANTS import *
from sprites import *
from forces import *

pygame.init()

SPAWN_WALL_RATE = 1000
SPAWN_WALL_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_WALL_EVENT, SPAWN_WALL_RATE)

scr = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player()
wall_fabric = WallFabric()
walls = pygame.sprite.Group()

multiplier = 1
score = 0
score_text = Score(score)

game = True
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.jump()
        if e.type == SPAWN_WALL_EVENT:
            walls.add(wall_fabric.create())
    
    scr.fill((0, 100, 255))
    
    game = player.update(scr, walls)
    
    for wall in walls.sprites():
        wall.update(scr)
    
    score += multiplier
    score_text.update(scr, score)
    
    clock.tick(FPS)
    pygame.display.flip()
    
pygame.quit()
