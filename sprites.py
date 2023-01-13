import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 500

# CONSTANTS

WHITE = (255, 255, 255)
STARTING_VELOCITY = 5
ACCELERATION = 1.0005

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

ROCKET_WIDTH, ROCKET_HEIGHT = 70, 45
MINE_DIM = 50
COIN_DIM = 30
JEWEL_DIM = 40
CLOCK_DIM = 30
EXPLOSION_DIM = 60

ROCKET = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'rocket.png')), (ROCKET_WIDTH, ROCKET_HEIGHT))

ROCKET_UP = pygame.transform.rotate(ROCKET, 10)
ROCKET_DOWN = pygame.transform.rotate(ROCKET, -10)

MINE = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'mine.png')), (MINE_DIM, MINE_DIM))

COIN = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'coin.png')), (COIN_DIM, COIN_DIM))

JEWEL = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'jewel.png')), (JEWEL_DIM, JEWEL_DIM))

CLOCK = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'clock.png')), (CLOCK_DIM, CLOCK_DIM))

EXPLOSION = pygame.transform.scale(
    pygame.image.load(
        os.path.join('graphics', 'explosion.png')), (EXPLOSION_DIM, EXPLOSION_DIM))


SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('graphics', 'wallpaper.jpg')), (WIDTH, HEIGHT))

# SOUND IMPORTS

BACKGROUND_MUSIC = pygame.mixer.Sound(
    os.path.join('sound', 'background-music.wav'))

COIN_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'coin.wav'))

TIMER_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'timer.wav'))

COUNTDOWN_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'contdown.wav'))

JEWEL_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'jewel.wav'))

LOSE_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'lose.wav'))

START_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'start.wav'))

LOSE_SOUND = pygame.mixer.Sound(
    os.path.join('sound', 'lose.wav'))

# OTHER IMPORTS

MAIN_FONT = pygame.font.SysFont('consolas', 30)


class Rocketship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = ROCKET
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

    def handle_clock_pickup(self, clocks_group):
        if pygame.sprite.spritecollide(self, clocks_group, True):
            TIMER_SOUND.play()
            self.vel = self.vel/1.5
            pygame.event.post(pygame.event.Event(CLOCK_START))

    def update(self, WIN):
        # moving:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and self.rect.y - self.vel > 0:  # UP
            self.rect.y -= self.vel
            self.image = ROCKET_UP
        elif keys_pressed[pygame.K_DOWN] and self.rect.y + self.vel + self.rect.height < HEIGHT:  # DOWN
            self.rect.y += self.vel
            self.image = ROCKET_DOWN
        else:
            self.image = ROCKET

        # rendering score:
        score_text = MAIN_FONT.render(
            "Score: " + str(self.score), 1, WHITE)

        WIN.blit(score_text,  (WIDTH/2 - score_text.get_width() //
                               2, 10))

        # increasing velocity
        self.vel *= ACCELERATION


class Mine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = MINE
        self.rect = self.image.get_rect()
        self.rect.center = [850, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = COIN
        self.rect = self.image.get_rect()
        self.rect.center = [850, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()


class Jewel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = JEWEL
        self.rect = self.image.get_rect()
        self.rect.center = [850, random.choice(range(10, 490))
                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()


class Slowed_Time(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = CLOCK
        self.rect = self.image.get_rect()
        self.rect.center = [850, random.choice(range(10, 490))

                            ]

    def update(self, vel):
        self.rect.x -= vel
        if self.rect.right <= -100:
            self.kill()
