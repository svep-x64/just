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
                    os.path.join(TEXTURES_DIR, texture)
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
    def __init__(self, lines_group):
        x, y = 200, HEIGHT / 2
        width, height = 40, 40

        super().__init__(x, y, width, height, texture="player.png")

        self.speed_y = Speed()
        # self.lines_group = lines_group  # постоянная группа линий
        # self.checker = False

    def jump(self):
        self.speed_y.set_v(-JUMPFORCE)

    def update(self, scr, walls, srngs):
        super().update(scr)

        # Движение игрока
        self.speed_y.update()
        self.y += G * self.speed_y.get_v()

        # Столкновения со шприцами
        self.colided_srngs = pygame.sprite.spritecollide(self, srngs, False)

        # --- Проверка линии и удаление при касании ---
        # for wall in walls:
        #     if not wall.scored and self.rect.colliderect(wall.center_line.rect):
        #         wall.scored = True          # очко только один раз
        #         wall.center_line.kill()     # удаляем линию
        #         score += 1
        #         self.checker = True
        # --- конец исправления ---

        # Столкновения со стенами
        self.collides = {
            "wall": pygame.sprite.spritecollide(self, walls, False),
            "syringe": self.colided_srngs,
            # "checker": self.checker
        }

        self.output = [self.collides, self.colided_srngs]

        if self.y > HEIGHT + 50 or self.y < -50:
            self.collides["wall"] = True

        # Обновление игрока на экране
        super().update(scr)

        return self.output


class Wall(Unit, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, facet=False):
        self.scored = False
        pygame.sprite.Sprite.__init__(self)

        if facet:
            super().__init__(x, y, width, height, texture="rotated_tube.png")
        else:
            super().__init__(x, y, width, height, texture="tube.png")

        self.speed = speed

        # self.center_line = pygame.sprite.Sprite()
        # self.center_line.image = pygame.Surface((2, HEIGHT))
        # self.center_line.image.fill((255, 0, 0))  # красная линия
        # self.center_line.rect = self.center_line.image.get_rect()
        # self.center_line.rect.centerx = self.rect.centerx
        # self.center_line.rect.top = 0

    def update(self, scr):
        super().update(scr)

        self.x -= self.speed
        # self.center_line.rect.centerx = self.rect.centerx
        # pygame.draw.rect(scr, (255, 0, 0), self.center_line)
        if self.x < -50:
            self.kill()


class WallFabric:
    def __init__(self):
        self.speed = 3

    def create(self):
        x = WIDTH + 100
        y1, y2 = HEIGHT, 0

        width = 100
        height1 = random.randint(100, HEIGHT)

        height2 = HEIGHT - height1 // 2 - 70

        Wall1 = Wall(x, y1, width, height1, self.speed)
        Wall2 = Wall(x, y2, width, height2, self.speed, facet=True)


        return Wall1, Wall2


class Syringe(Unit, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(x, y, width, height, texture="syringe.png")

        self.speed = speed

    def update(self, scr):
        super().update(scr)
        self.x -= self.speed

        if self.x < -30:
            self.kill()


class SyringeFabric:
    def __init__(self):
        self.speed = 6

    def create(self):
        x = WIDTH + 100
        y = random.randint(150, HEIGHT-150)

        width = SYRINGE_WIDTH
        height = SYRINGE_HEIGHT

        syringe = Syringe(x, y, width, height, self.speed)

        return syringe


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