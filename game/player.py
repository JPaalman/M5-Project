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

        self.x = x  # x position
        self.y = y  # y position
        self.h = h  # height
        self.w = w  # width

        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, self.GRAVITY)

        self.rect = pg.Rect(x, y, w, h)

        self.image = pg.Surface(w, h)
        self.image.fill(RED)
        # self.image = pg.image.load("../resources/player.*")

    def update(self):
        """
        I'm also a docstring hurr durr
        """

        # key updates
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x -= self.a
        if keys[pg.K_RIGHT]:
            self.acc.x += self.a
        # test jumping function
        if keys[pg.K_SPACE]:
            self.vel.y = -20

        # friction
        self.acc.x -= self.vel.x * self.FRICTION

        # update vel and pos
        self.vel.x += self.acc.x
        self.x += self.vel.x

        self.vel.y += self.acc.y
        self.y += self.vel.y

        # dummy collision
        if self.y > 700:
            self.y = 700
