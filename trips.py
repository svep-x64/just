import random

from CONSTANTS import *

import math
import os.path
import numpy as np
import pygame


def effect_vibe(surface):
    width, height = surface.get_size()
    new_surface = pygame.Surface((width, height)).convert_alpha()
    new_surface.fill((0, 0, 0, 0))

    time = pygame.time.get_ticks() / 1000
    amplitude = 15
    frequency = 0.05

    for y in range(height):
        offset_x = int(math.sin(y * frequency + time) * amplitude + math.sin(time + y * 0.1) * 3)
        new_surface.blit(surface, (offset_x, y), area=pygame.Rect(0, y, width, 1))

    rect = new_surface.get_rect()
    return new_surface, rect


def effect_wave(surface):
    width, height = surface.get_size()
    result = pygame.Surface((width, height))
    time = pygame.time.get_ticks()

    for y in range(height):
        offset = int(20 * math.sin(y * 0.02 + time * 0.005))
        result.blit(surface, (offset, y), (0, y, width, 1))

    return result, result.get_rect(topleft=(0, 0))


def effect_spin(surface):
    width, height = surface.get_size()
    time = pygame.time.get_ticks()

    scale = 1 + 0.08 * math.sin(time * 0.005)

    rotated = pygame.transform.rotozoom(
        surface,
        time * 0.05,
        scale
    )

    rect = rotated.get_rect(center=(width // 2, height // 2))
    return rotated, rect

def effect_invert(surface):
    arr = pygame.surfarray.array3d(surface)
    arr = 255 - arr
    result = pygame.surfarray.make_surface(arr)
    return result, result.get_rect(topleft=(0, 0))


def effect_rgb(surface):
    width, height = surface.get_size()

    scale = 0.2
    small_w, small_h = max(1, int(width * scale)), max(1, int(height * scale))
    small_surf = pygame.transform.smoothscale(surface, (small_w, small_h))

    arr = pygame.surfarray.pixels3d(small_surf).astype(np.int16)

    time = pygame.time.get_ticks() / 150

    yy, xx = np.meshgrid(np.arange(small_h), np.arange(small_w), indexing='ij')
    dx = xx - small_w // 2
    dy = yy - small_h // 2
    dist = np.hypot(dx, dy)

    wave = np.sin(dist * 0.08 - time) * 127 + 128

    r = (arr[:, :, 0] + wave.T) % 256
    g = (arr[:, :, 1] + np.sin(wave.T * 0.024 * math.pi) * 128) % 256
    b = (arr[:, :, 2] + np.cos(wave.T * 0.018 * math.pi) * 128) % 256

    arr[:, :, 0] = r.astype(np.uint8)
    arr[:, :, 1] = g.astype(np.uint8)
    arr[:, :, 2] = b.astype(np.uint8)

    new_surf = pygame.surfarray.make_surface(arr)
    new_surf = pygame.transform.smoothscale(new_surf, (width, height))

    return new_surf, new_surf.get_rect()

def set_all_texture(surface, walls, srngs, player, path):
    texture = pygame.transform.scale(
        pygame.image.load(os.path.join(TEXTURES_DIR, path)).convert_alpha(),
        (WIDTH, HEIGHT)
    )

    result = texture.copy()

    all_sprites = list(walls.sprites()) + list(srngs.sprites()) + [player]

    for sprite in all_sprites:
        x, y = sprite.rect.topleft
        w, h = sprite.rect.size

        tex = pygame.transform.scale(texture, (w, h))

        mask = pygame.mask.from_surface(sprite.image)
        mask_surf = mask.to_surface(setcolor=(255,255,255,255), unsetcolor=(0,0,0,0))
        mask_surf.set_alpha(255)

        tex.blit(mask_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

        result.blit(tex, (x, y))

    return result, result.get_rect(topleft=(0, 0))

def effect_milana(surface, walls, srngs, player):
    result, rect = set_all_texture(surface, walls, srngs, player, "milana.png")
    return result, rect


def mirror_effect(surface):
    mirrored = pygame.transform.flip(surface, True, False)
    rect = mirrored.get_rect()

    return mirrored, rect

def glitch_effect(surface):
    variants = ["osel.png", "milana.png", "shailushai.png", "bird.png", "skebob.png", "b.png", "bu.png", "kalivan.png"]

    for _ in range(len(variants)*5):
        variants.append(0)

    glitch = random.choice(variants)

    if glitch != 0:
        pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "glitch.mp3")).play()

        image = pygame.image.load(os.path.join(TEXTURES_DIR, glitch)).convert_alpha()
        image = pygame.transform.scale(image, surface.get_size())

        result = surface.copy()
        result.blit(image, (0, 0))
    else:
        result = surface

    return result, result.get_rect()

SOUNDS = {
    effect_wave:"bing_bing_boo.mp3",
    effect_spin:"spin.mp3",
    effect_vibe:"vibe.mp3",
    effect_invert:"bg_music_inverted.mp3",
    effect_rgb:"rgb.mp3",
    effect_milana:"grustniy_track_sk.mp3",
    mirror_effect:"bg_music_reversed.mp3",
    glitch_effect:""
}