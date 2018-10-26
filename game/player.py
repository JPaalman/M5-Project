import pygame as pg

from game.settings import *


class Player(pg.sprite.Sprite):
    """
    I'm a docstring hurr durr
    """
    ACCELERATION = 60 / FPS  # dummy value
    FRICTION = 1  # dummy value
    GRAVITY = 1  # dummy value
    LIFE = 5

    def __init__(self, x, y, h, w):
        super().__init__()

        self.x = x  # horizontal position
        self.y = y  # vertical position
        self.h = h  # height
        self.w = w  # width

        self.vel = pg.Vector2(0, 0)  # velocity
        self.acc = pg.Vector2(0, self.GRAVITY)  # acceleration

        self.rect = pg.Rect(x, y, w, h)

        self.image = pg.Surface(w, h)
        self.image.fill(RED)
        # self.image = pg.image.load("../resources/player.*")

    def update(self):
        """
        I'm also a docstring hurr durr
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x -= self.ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x += self.ACCELERATION
        if keys[pg.K_SPACE]:
            self.vel.y = -20

        self.acc.x -= self.vel.x * self.FRICTION

        self.vel.x += self.acc.x
        self.x += self.vel.x

        self.vel.y += self.acc.y
        self.y += self.vel.y

        # dummy collision
        if self.y > 700:
            self.y = 700
