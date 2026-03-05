import os.path

from CONSTANTS import *

import pygame
import json
import sys

def load_image(name, scale):
    img = pygame.image.load(os.path.join(TEXTURES_DIR, name)).convert_alpha()
    img = pygame.transform.scale(img, scale)

    return img
def get_setting(key):
    with open(os.path.join(ROOT_DIR, "settings.json"), "r") as f:
        data = json.load(f)
        if key in data:
            return data[key]

def set_setting(key, value):
    with open(os.path.join(ROOT_DIR, "settings.json"), "r") as f:
        data = json.load(f)
    with open(os.path.join(ROOT_DIR, "settings.json"), "w") as f:
        data[key] = value
        if key in data:
            json.dump(data, f, indent=4)


def create_text(text, x, y, font, screen):
    text = font.render(text, True, (43, 10, 61))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)


class Switch:
    def __init__(self, x, y, width=80, height=40, initial=False):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.state = initial
        self.knob_radius = height // 2 - 4
        self.knob_x = self.rect.x + (self.rect.width - self.knob_radius * 2 - 4 if self.state else 4)
        self.animation_speed = 8
        self.target_x = self.knob_x

        self.color_on = (100, 255, 100)
        self.color_off = (180, 180, 180)
        self.knob_color = (255, 255, 255)

    def draw(self, surface):
        color = self.color_on if self.state else self.color_off
        pygame.draw.rect(surface, color, self.rect, border_radius=self.rect.height // 2)
        pygame.draw.circle(surface, self.knob_color, (int(self.knob_x + self.knob_radius), self.rect.centery),
                           self.knob_radius)

    def update(self):
        if self.state:
            self.target_x = self.rect.right - self.knob_radius * 2 - 4
        else:
            self.target_x = self.rect.x + 4

        if self.knob_x < self.target_x:
            self.knob_x += self.animation_speed
            if self.knob_x > self.target_x:
                self.knob_x = self.target_x
        elif self.knob_x > self.target_x:
            self.knob_x -= self.animation_speed
            if self.knob_x < self.target_x:
                self.knob_x = self.target_x

    def handle_event(self, event):
        # переключение состояния при клике
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state

    def get_coordinates(self):
        return self.x, self.y

    def get_initial(self):
        return self.state


class SettingsMenu:
    def __init__(self, screen, clock, start_menu_callback):
        self.screen = screen
        self.clock = clock
        self.menu_callback = start_menu_callback
        self.font = pygame.font.SysFont("Arial", 25)

        self.background = pygame.image.load(os.path.join(TEXTURES_DIR, "settings_bg.png")).convert()
        self.background = pygame.transform.scale(self.background, (SETTINGS_WIDTH, SETTINGS_HEIGHT))

        self.hitbox_switch1 = Switch(400, 30, initial=get_setting("death_hitboxes"))
        self.hitbox_switch2 = Switch(400, 85, initial=get_setting("restart"))

        self.back_button_img = load_image("back.png", (174, 115))
        self.hover_back_button_img = load_image("hover_back.png", (174, 115))
        self.button_rect = pygame.Rect(170, 500, 174, 115)

        self.switchers = {
            self.hitbox_switch1: "death_hitboxes",
            self.hitbox_switch2: "restart"
        }

    def run(self):

        self.running = True

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.background, (0, 0))

            if self.button_rect.collidepoint(mouse_pos):
                self.screen.blit(self.hover_back_button_img, self.button_rect.topleft)
            else:
                self.screen.blit(self.back_button_img, self.button_rect.topleft)

            create_text("Хитбоксы после смерти", 170, 50, self.font, self.screen)
            create_text("Моментальный рестарт", 170, 100, self.font, self.screen)

            for switcher in self.switchers:
                switcher.update()
                switcher.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                for switcher in self.switchers:
                    switcher.handle_event(event)
                    key = self.switchers[switcher]
                    value = switcher.get_initial()

                    set_setting(key, value)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if self.button_rect.collidepoint(mouse_pos):
                        self.running = False
                        self.menu_callback()
            self.clock.tick(30)

        # self.new_screen = pygame.display.set_mode((SETTINGS_WIDTH, SETTINGS_HEIGHT)
        # main_menu = MainMenu(self.new_screen, self.clock)
        # main_menu.run()



