from sprites import *
from MainMenu import *
from trips import *
from random import randint as rd, choice
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()
game_surface = pygame.Surface((WIDTH, HEIGHT))
scr = pygame.display.set_mode((WIDTH, HEIGHT))

bg_music = os.path.join(SOUNDS_DIR, "bg_music.mp3")
mixer = pygame.mixer
bg_sound = mixer.Sound(bg_music)

pygame.display.set_caption("DruggyBird")


def game_loop():
    SPAWN_WALL_RATE = 1000
    SPAWN_WALL_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_WALL_EVENT, SPAWN_WALL_RATE)

    background_img = pygame.image.load(os.path.join(TEXTURES_DIR, "background.png")).convert()

    wall_fabric = WallFabric()
    walls = pygame.sprite.Group()
    lines = pygame.sprite.Group()

    player = Player(lines)

    syringe_fabric = SyringeFabric()
    srngs = pygame.sprite.Group()
    srngs.add(syringe_fabric.create())

    score = 0
    score_text = Stroke(score)

    game = True
    ADSKIY_PIZDEC = False  # К сожелению

    trip = None
    previous = None

    bg_sound.play()
    bg_sound.set_volume(0.5)

    while game:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE or e.key == pygame.K_UP:
                    player.jump()
            if e.type == SPAWN_WALL_EVENT:
                walls.add(wall_fabric.create())
                if rd(1, 3) == 2:
                    srngs.add(syringe_fabric.create())

        update_data = player.update(game_surface, walls, srngs)
        game = not update_data[0]["wall"]
        trip_flag = bool(update_data[0]["syringe"])

        pygame.display.flip()

        if trip_flag:
            ADSKIY_PIZDEC = trip_flag

        game_surface.blit(background_img, (0, 0))
        colided_syringes = player.update(game_surface, walls, srngs)[1]
        # colide_checker = update_data[0]["checker"]

        if colided_syringes:
            mixer.music.stop()
            bg_sound.stop()

            use_sound = mixer.Sound(os.path.join(SOUNDS_DIR, "syringe_use.mp3"))
            use_sound.play()
            use_sound.set_volume(1)

            trips = list(SOUNDS.keys())

            if previous is None and trip is None:
                trip = choice(trips)
            else:
                trip = choice(trips)
                while trip == previous:
                    trip = choice(trips)

            previous = trip

            if ADSKIY_PIZDEC and trip is not None:
                mixer.music.stop()
                if trip in SOUNDS:
                    try:
                        mixer.music.load(os.path.join(SOUNDS_DIR, SOUNDS[trip]))
                        mixer.music.play(-1)
                    except:
                        pass

            for i in colided_syringes:
                i.kill()

        for wall in walls.sprites():
            wall.update(game_surface)
        for syringe in srngs.sprites():
            syringe.update(game_surface)

        # if colide_checker:
        #     score += 1
        score_text.update(game_surface, score)

        clock.tick(FPS)

        if ADSKIY_PIZDEC and trip is not None:
            if trip == effect_milana:
                effected_surface, rect = effect_milana(game_surface, walls, srngs, player)
            elif trip == effect_video:
                effected_surface, rect = effect_video(game_surface, mixer)
            else:
                effected_surface, rect = trip(game_surface)
            scr.blit(effected_surface, rect)
        else:
            scr.blit(game_surface, (0, 0))

    mixer.music.stop()
    bg_sound.stop()
    mixer.Sound(os.path.join(SOUNDS_DIR, "fail.mp3")).play()


mixer.music.stop()
bg_sound.stop()

menu = MainMenu(
    scr, clock,
    start_game_callback=game_loop,
    links_url="https://github.com/svep-x64/just/tree/shuraa"
)
menu.run()

