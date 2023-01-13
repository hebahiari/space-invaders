import pygame
import os
import random
import sys

WIDTH, HEIGHT = 900, 500
ROCKET_WIDTH, ROCKET_HEIGHT = 70, 45
MINE_DIM = 50
COIN_DIM = 30
JEWEL_DIM = 40
CLOCK_DIM = 30
EXPLOSION_DIM = 60


class Rocketship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'rocket.png')), (ROCKET_WIDTH, ROCKET_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def move(self, vel):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] and self.rect.y - vel > 0:  # UP
            self.rect.y -= vel
        if keys_pressed[pygame.K_DOWN] and self.rect.y + vel + self.rect.height < HEIGHT:  # DOWN
            self.rect.y += vel


class Mines(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super.__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join('Assets', 'mine.png')), (MINE_DIM, MINE_DIM))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
