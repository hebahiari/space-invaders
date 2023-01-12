import pygame
import os
import random
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
VEL = 5
ACCELERATION = 1.5
MAX_BULLETS = 3

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

ROCKET_WIDTH, ROCKET_HEIGHT = 41, 77
MINE_DIM = 50
COIN_DIM = 30
JEWEL_DIM = 40
CLOCK_DIM = 30
EXPLOSION_DIM = 60

ROCKET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'rocket1.png'))
ROCKET = pygame.transform.rotate(pygame.transform.scale(
    ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT)), 270)

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

EXPLOSION_IMAGE = pygame.image.load(
    os.path.join('Assets', 'explosion.png'))
EXPLOSION = pygame.transform.scale(
    EXPLOSION_IMAGE, (EXPLOSION_DIM, EXPLOSION_DIM))


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


def draw_window(rocket, mines, jewels, coins, score
                ):
    WIN.blit(SPACE, (0, 0))
    # pygame.draw.rect(WIN, BLACK, BARRIER)

    score_text = MAIN_FONT.render(
        "Score: " + str(score), 1, WHITE)

    WIN.blit(score_text,  (WIDTH/2 - score_text.get_width() //
             2, 10))

    # WIN.blit() adds items to the screen like text or objects
    WIN.blit(ROCKET, (rocket.x, rocket.y))

    for mine in mines:
        WIN.blit(MINE, (mine.x, mine.y))

    for jewel in jewels:
        WIN.blit(JEWEL, (jewel.x, jewel.y))

    for coin in coins:
        WIN.blit(COIN, (coin.x, coin.y))

    pygame.display.update()


def rocket_handle_movement(keys_pressed, rocket):
    if keys_pressed[pygame.K_UP] and rocket.y - VEL > 0:  # UP
        rocket.y -= VEL
    if keys_pressed[pygame.K_DOWN] and rocket.y + VEL + rocket.height < HEIGHT:  # DOWN
        rocket.y += VEL


def handle_mines(mines, rocket):
    for mine in mines:
        mine.x -= VEL
        if mine.x < 0 - MINE_DIM:
            mines.remove(mine)
        if rocket.colliderect(mine):
            pygame.event.post(pygame.event.Event(MINE_HIT))

            # pygame.event.post(pygame.event.Event(COIN_COLLECT))
            # yellow_bullets.remove(bullet)


def handle_jewels(jewels, rocket):
    for jewel in jewels:
        jewel.x -= VEL
        if jewel.x < 0 - JEWEL_DIM:
            jewels.remove(jewel)
        if rocket.colliderect(jewel):
            JEWEL_SOUND.play()
            pygame.event.post(pygame.event.Event(JEWEL_COLLECT))
            jewels.remove(jewel)


def handle_coins(coins, rocket):
    for coin in coins:
        coin.x -= VEL
        if coin.x < 0 - COIN_DIM:
            coins.remove(coin)
        if rocket.colliderect(coin):
            COIN_SOUND.play()
            pygame.event.post(pygame.event.Event(COIN_COLLECT))
            coins.remove(coin)


def draw_lost(text, explosion, rocket):
    draw_text = MAIN_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() //
             2, HEIGHT/2 - draw_text.get_height()//2))
    WIN.blit(EXPLOSION, (explosion.x, explosion.y))

    while rocket.y < 400:
        rocket.y += VEL
    pygame.display.update()
    pygame.time.delay(5000)


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

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == COIN_COLLECT:
                score += 1

            if event.type == CLOCK_COLLECT:
                TIMER_SOUND.play()

            if event.type == JEWEL_COLLECT:
                score += 5

            if event.type == CREATE_MINE:
                y = random.choice(range(10, 490))
                mines.append(pygame.Rect(900, y, MINE_DIM, MINE_DIM))

            if event.type == CREATE_JEWEL:
                y = random.choice(range(10, 490))
                jewels.append(pygame.Rect(900, y, JEWEL_DIM, JEWEL_DIM))

            if event.type == CREATE_COIN:
                y = random.choice(range(10, 490))
                coins.append(pygame.Rect(900, y, COIN_DIM, COIN_DIM))

            if event.type == MINE_HIT:
                LOSE_SOUND.play()
                explosion = pygame.Rect(
                    rocket.x + ROCKET_WIDTH - 10, rocket.y, EXPLOSION_DIM, EXPLOSION_DIM)
                draw_lost("you lost!", explosion, rocket)
                main()

        keys_pressed = pygame.key.get_pressed()
        rocket_handle_movement(keys_pressed, rocket)

        handle_mines(mines, rocket)
        handle_jewels(jewels, rocket)
        handle_coins(coins, rocket)

        draw_window(rocket, mines, jewels, coins, score
                    )

    main()


if __name__ == "__main__":
    main()
