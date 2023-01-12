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
BULLET_VEL = 7
MAX_BULLETS = 3

# EVENTS

MINE_HIT = pygame.USEREVENT + 1
COIN_COLLECT = pygame.USEREVENT + 2
JEWEL_COLLECT = pygame.USEREVENT + 3
CLOCK_COLLECT = pygame.USEREVENT + 4
CREATE_MINE = pygame.USEREVENT + 5

# IMPORTS

# IMAGE IMPORTS

ROCKET_WIDTH, ROCKET_HEIGHT = 41, 77
MINE_DIM = 50
COIN_DIM = 25
JEWEL_DIM = 25
CLOCK_DIM = 30

ROCKET_IMAGE = pygame.image.load(
    os.path.join('Assets', 'rocket1.png'))
ROCKET = pygame.transform.rotate(pygame.transform.scale(
    ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HEIGHT)), 270)

MINE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'mine.png'))
MINE = pygame.transform.rotate(pygame.transform.scale(
    MINE_IMAGE, (MINE_DIM, MINE_DIM)), 270)

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

MAIN_FONT = pygame.font.SysFont('pixel', 40)

# FUNCTION DEFINITIONS


def draw_window(rocket, mines, red_bullets, yellow_bullets
                ):
    WIN.blit(SPACE, (0, 0))
    # pygame.draw.rect(WIN, BLACK, BARRIER)

    # red_health_text = MAIN_FONT.render(
    #     "Health: " + str(red_health), 1, WHITE)
    # yellow_health_text = MAIN_FONT.render(
    #     "Health: " + str(yellow_health), 1, WHITE)
    # WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    # WIN.blit(yellow_health_text, (10, 10))

    # WIN.blit() adds items to the screen like text or objects
    WIN.blit(ROCKET, (rocket.x, rocket.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for mine in mines:
        WIN.blit(MINE, (mine.x, mine.y))
        mine.x -= VEL
        if mine.x < 0 - MINE_DIM:
            mines.remove(mine)
        print(mines)

    pygame.display.update()


def rocket_handle_movement(keys_pressed, rocket):
    if keys_pressed[pygame.K_UP] and rocket.y - VEL > 0:  # UP
        rocket.y -= VEL
    if keys_pressed[pygame.K_DOWN] and rocket.y + VEL + rocket.height < HEIGHT:  # DOWN
        rocket.y += VEL


def handle_bullets(yellow_bullets, red_bullets, rocket):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if rocket.colliderect(bullet):
            pygame.event.post(pygame.event.Event(COIN_COLLECT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


def draw_winner(text):
    draw_text = MAIN_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() //
             2, HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    pygame.time.set_timer(CREATE_MINE, random.randrange(2000, 3500))
    # pycame.Rect() to basically define a rectangle to represent our object
    rocket = pygame.Rect(100, 350, ROCKET_WIDTH, ROCKET_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    mines = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == COIN_COLLECT:
                COIN_SOUND.play()

            if event.type == JEWEL_COLLECT:
                JEWEL_SOUND.play()

            if event.type == CLOCK_COLLECT:
                TIMER_SOUND.play()

            if event.type == CREATE_MINE:
                y = random.choice(range(10, 490))
                mines.append(pygame.Rect(900, y, MINE_DIM, MINE_DIM))

            if event.type == MINE_HIT:
                LOSE_SOUND.play()
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        rocket_handle_movement(keys_pressed, rocket)

        handle_bullets(yellow_bullets, red_bullets, rocket)

        draw_window(rocket, mines, red_bullets, yellow_bullets
                    )

    main()


if __name__ == "__main__":
    main()
