import pygame
import os
import random
import sys

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
STARTING_VELOCITY = 5

# EVENTS

MINE_HIT = pygame.USEREVENT + 1
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

EXPLOSION_IMAGE = pygame.image.load(
    os.path.join('Assets', 'explosion.png'))
EXPLOSION = pygame.transform.scale(
    EXPLOSION_IMAGE, (EXPLOSION_DIM, EXPLOSION_DIM))


LOSE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'lose.wav'))


class Rocketship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'rocket.png')), (ROCKET_WIDTH, ROCKET_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.score = 0
        self.vel = STARTING_VELOCITY

    def handle_mine_collision(self, mines_group, WIN):
        if pygame.sprite.spritecollide(self, mines_group, True):
            LOSE_SOUND.play()

            explosion = pygame.Rect(
                self.rect.x, self.rect.y, EXPLOSION_DIM, EXPLOSION_DIM)
            draw_text = MAIN_FONT.render("Game Over!", 1, WHITE)
            WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() //
                                 2, HEIGHT/2 - draw_text.get_height()//2))
            WIN.blit(EXPLOSION, (explosion.x, explosion.y))

            pygame.display.update()
            pygame.time.delay(5000)
            pygame.event.post(pygame.event.Event(MINE_HIT))

    def handle_coin_pickup(self, coins_group):
        if pygame.sprite.spritecollide(self, coins_group, True):
            COIN_SOUND.play()
            self.score += 1

    def handle_jewel_pickup(self, jewels_group):
        if pygame.sprite.spritecollide(self, jewels_group, True):
            JEWEL_SOUND.play()
            self.score += 5

    def update(self):
        # moving:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and self.rect.y - self.vel > 0:  # UP
            self.rect.y -= self.vel
        if keys_pressed[pygame.K_DOWN] and self.rect.y + self.vel + self.rect.height < HEIGHT:  # DOWN
            self.rect.y += self.vel

        # rendering score:
        score_text = MAIN_FONT.render(
            "Score: " + str(self.score), 1, WHITE)

        WIN.blit(score_text,  (WIDTH/2 - score_text.get_width() //
                               2, 10))

        # increasing velocity
        self.vel += .001


class Mine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'mine.png')), (MINE_DIM, MINE_DIM))
        self.rect = self.image.get_rect()
        self.rect.center = [900, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'coin.png')), (COIN_DIM, COIN_DIM))
        self.rect = self.image.get_rect()
        self.rect.center = [900, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()


class Jewel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'jewel.png')), (JEWEL_DIM, JEWEL_DIM))
        self.rect = self.image.get_rect()
        self.rect.center = [900, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()
