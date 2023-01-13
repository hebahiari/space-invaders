import pygame
import os
import random
import sys
from sprites import Rocketship, Mine, Coin

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (225, 255, 0)

FPS = 60
# vel = 5
ACCELERATION = 1.5

# EVENTS

MINE_HIT = pygame.USEREVENT + 1
COIN_COLLECT = pygame.USEREVENT + 2
JEWEL_COLLECT = pygame.USEREVENT + 3
CLOCK_COLLECT = pygame.USEREVENT + 4
CREATE_MINE = pygame.USEREVENT + 5
CREATE_JEWEL = pygame.USEREVENT + 6
CREATE_COIN = pygame.USEREVENT + 7

# IMPORTS

# IMAGE IMPORTS

ROCKET_WIDTH, ROCKET_HEIGHT = 70, 45
MINE_DIM = 50
COIN_DIM = 30
JEWEL_DIM = 40
CLOCK_DIM = 30
EXPLOSION_DIM = 60


ROCKET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'rocket.png'))
ROCKET = pygame.transform.scale(
    ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT))

MINE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'mine.png'))
MINE = pygame.transform.scale(
    MINE_IMAGE, (MINE_DIM, MINE_DIM))

COIN_IMAGE = pygame.image.load(
    os.path.join('Assets', 'coin.png'))
COIN = pygame.transform.scale(
    COIN_IMAGE, (COIN_DIM, COIN_DIM))

JEWEL_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jewel.png'))
JEWEL = pygame.transform.scale(
    JEWEL_IMAGE, (JEWEL_DIM, JEWEL_DIM))

CLOCK_IMAGE = pygame.image.load(
    os.path.join('Assets', 'jewel.png'))
CLOCK = pygame.transform.scale(
    CLOCK_IMAGE, (CLOCK_DIM, CLOCK_DIM))


SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'wallpaper.jpg')), (WIDTH, HEIGHT))

# SOUND IMPORTS

BACKGROUND_MUSIC = pygame.mixer.Sound(
    os.path.join('Assets', 'background-music.wav'))

COIN_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'coin.wav'))

TIMER_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'timer.wav'))

COUNTDOWN_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'contdown.wav'))

JEWEL_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'jewel.wav'))

LOSE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'lose.wav'))

START_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'start.wav'))

# OTHER IMPORTS

MAIN_FONT = pygame.font.SysFont('consolas', 30)

# FUNCTION DEFINITIONS


def draw_window(jewels, coins, score, rocketship_group, mines_group, coins_group
                ):
    WIN.blit(SPACE, (0, 0))
    # pygame.draw.rect(WIN, BLACK, BARRIER)
    rocketship_group.draw(WIN)
    rocketship_group.update()
    mines_group.draw(WIN)
    coins_group.draw(WIN)
    mines_group.update()
    coins_group.update()

    # score_text = MAIN_FONT.render(
    #     "Score: " + str(score), 1, WHITE)

    # WIN.blit(score_text,  (WIDTH/2 - score_text.get_width() //
    #          2, 10))

    pygame.display.update()


def handle_jewels(jewels, rocket, vel):
    for jewel in jewels:
        jewel.x -= vel
        if jewel.x < 0 - JEWEL_DIM:
            jewels.remove(jewel)
        if rocket.colliderect(jewel):
            JEWEL_SOUND.play()
            pygame.event.post(pygame.event.Event(JEWEL_COLLECT))
            jewels.remove(jewel)


def draw_winner(text):
    draw_text = MAIN_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() //
             2, HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    pygame.time.set_timer(CREATE_MINE, 1500)
    pygame.time.set_timer(CREATE_JEWEL, 8000)
    pygame.time.set_timer(CREATE_COIN, 800)

    # pycame.Rect() to basically define a rectangle to represent our object
    rocket = pygame.Rect(100, 350, ROCKET_WIDTH, ROCKET_HEIGHT)

    coins = []
    jewels = []
    mines = []
    score = 0
    vel = 5

# rocketship
    rocketship = Rocketship(100, 250)
    rocketship_group = pygame.sprite.Group()
    rocketship_group.add(rocketship)

# mines
    mines_group = pygame.sprite.Group()

# coins
    coins_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    run = True
    while run:
        vel += .001

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == COIN_COLLECT:
                score += 1

            if event.type == CLOCK_COLLECT:
                TIMER_SOUND.play()

            if event.type == JEWEL_COLLECT:
                score += 5

            if event.type == CREATE_MINE:
                mines_group.add(Mine())

            if event.type == CREATE_JEWEL:
                coins_group.add(Coin())

            if event.type == CREATE_COIN:
                coins_group.add(Coin())

            if event.type == MINE_HIT:
                main()

        rocketship.move(vel, mines_group)
        rocketship.handle_mine_collision(mines_group, WIN)
        rocketship.handle_coin_pickup(coins_group)
        # handle_jewels(jewels, rocket, vel)
        # handle_coins(coins, rocket, vel)
        draw_window(jewels, coins, score, rocketship_group, mines_group, coins_group
                    )

    main()


if __name__ == "__main__":
    main()
