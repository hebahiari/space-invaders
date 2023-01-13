import pygame
import os
import sys
from sprites import Rocketship, Mine, Coin, Jewel, Slowed_Time

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# CONSTANTS

WHITE = (255, 255, 255)
FPS = 60

# EVENTS

MINE_HIT = pygame.USEREVENT + 1
CREATE_MINE = pygame.USEREVENT + 2
CREATE_JEWEL = pygame.USEREVENT + 3
CREATE_COIN = pygame.USEREVENT + 4
CREATE_CLOCK = pygame.USEREVENT + 5
CLOCK_START = pygame.USEREVENT + 6
CLOCK_END = pygame.USEREVENT + 7


# IMPORTS

# IMAGE IMPORTS

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('graphics', 'wallpaper.jpg')), (WIDTH, HEIGHT))

# SOUND IMPORTS

BACKGROUND_MUSIC = pygame.mixer.Sound(
    os.path.join('sound', 'background-music.wav'))

COUNTDOWN_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'contdown.wav'))

START_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'start.wav'))

# OTHER IMPORTS

MAIN_FONT = pygame.font.SysFont('consolas', 30)

# FUNCTION DEFINITIONS


def main():

    pygame.time.set_timer(CREATE_MINE, 1500)
    pygame.time.set_timer(CREATE_JEWEL, 6000)
    pygame.time.set_timer(CREATE_COIN, 800)
    pygame.time.set_timer(CREATE_CLOCK, 13000)

# rocketship

    rocketship = Rocketship(100, 250)
    rocketship_group = pygame.sprite.Group()
    rocketship_group.add(rocketship)

# collectibles
    mines_group = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    jewels_group = pygame.sprite.Group()
    clocks_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    BACKGROUND_MUSIC.play()

    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == CREATE_MINE:
                mines_group.add(Mine())

            if event.type == CREATE_JEWEL:
                jewels_group.add(Jewel())

            if event.type == CREATE_COIN:
                coins_group.add(Coin())

            if event.type == CREATE_CLOCK:
                clocks_group.add(Slowed_Time())

            if event.type == CLOCK_END:
                rocketship.vel = rocketship.vel * 1.5

            if event.type == CLOCK_START:
                pygame.time.set_timer(CLOCK_END, 3000, 1)

            if event.type == MINE_HIT:
                main()

        rocketship.handle_mine_collision(mines_group, WIN)
        rocketship.handle_coin_pickup(coins_group)
        rocketship.handle_jewel_pickup(jewels_group)
        rocketship.handle_clock_pickup(clocks_group)

        WIN.blit(SPACE, (0, 0))
        rocketship_group.draw(WIN)
        mines_group.draw(WIN)
        coins_group.draw(WIN)
        jewels_group.draw(WIN)
        clocks_group.draw(WIN)
        rocketship_group.update(WIN)
        mines_group.update(rocketship.vel)
        coins_group.update(rocketship.vel)
        jewels_group.update(rocketship.vel)
        clocks_group.update(rocketship.vel)

        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
