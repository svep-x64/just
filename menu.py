import os.path

import pygame
import sys
import webbrowser
from CONSTANTS import *

def load_image(name, scale):
    img = pygame.image.load(os.path.join(TEXTURES_DIR, name)).convert_alpha()
    img = pygame.transform.scale(img, scale)

    return img
class MainMenu:
    def __init__(self, screen, clock, start_game_callback, links_url=None, font=None):
        self.screen = screen
        self.clock = clock
        self.start_game_callback = start_game_callback
        self.links_url = links_url
        self.font = font or pygame.font.SysFont("Arial", 32)
        self.font2 = font or pygame.font.SysFont("Arial", 15)

        self.background = pygame.image.load(os.path.join(TEXTURES_DIR, "menu_bg.png")).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.start_button_img = load_image("play.png", (246, 164))
        self.hover_start_button_img = load_image("play_hover.png", (246, 164))

        self.how_button_img = load_image("how_to_play.png", (246, 164))
        self.hover_how_button_img = load_image("hover_how_to_play.png", (246, 164))

        self.how_button_img = load_image("how_to_play.png", (246, 164))
        self.hover_how_button_img = load_image("hover_how_to_play.png", (246, 164))

        self.gh_button_img = load_image("gh_button.png", (246, 164))
        self.hover_gh_button_img = load_image("hovered_gh_button.png", (246, 164))

        self.buttons = [
            {"hover":self.hover_start_button_img, "image":self.start_button_img, "rect": pygame.Rect(10, 200, 246, 164)},
            {"hover":self.hover_how_button_img, "image":self.how_button_img, "rect": pygame.Rect(550, 206, 246, 164)},
            {"hover": self.hover_gh_button_img, "image": self.gh_button_img, "rect": pygame.Rect(280, 360, 176, 117)}
        ]

    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.screen.blit(button["hover"], button["rect"].topleft)
            self.screen.blit(button["image"], button["rect"].topleft)


    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.draw_buttons()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if self.buttons[0]["rect"].collidepoint(mouse_pos):
                        self.start_game_callback()
                    elif self.buttons[2]["rect"].collidepoint(mouse_pos) and self.links_url:
                        webbrowser.open(self.links_url)

            self.clock.tick(60)