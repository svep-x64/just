import pygame

pygame.init()

WIDTH, HEIGHT = 800, 500

scr = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = True

class Player:
    def __init__(self):       
        self.width, self.height = 50, 50
        x, y = 200, HEIGHT / 2
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 255))
        
        self.rect = self.image.get_rect()
        
        self.x, self.y = x, y
        self.move()

    def move(self):
        self.rect.center = (self.x, self.y)

    def update(self, scr):
        print(self.x, self.y)
        self.move()
        
        scr.blit(self.image, self.rect)

player = Player()

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    
    scr.fill((0, 0, 0))
    
    player.update(scr)
    
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()