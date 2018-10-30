import pygame as pg

from game.game import get_map
from settings import *
from utils import Vector

ACCELERATION = 1  # dummy value
FRICTION = 0  # dummy value
GRAVITY = 0.5  # dummy value
LIFE = 5


class Player(pg.sprite.Sprite):
    """
    I'm a docstring hurr durr
    """

    def __init__(self, x, y):
        super().__init__()

        self.moveLeft = False
        self.moveRight = False
        self.jump = False

        self.x = x  # horizontal position
        self.y = y  # vertical position
        self.w = TILESIZE
        self.h = TILESIZE * 1.5

        self.pos = Vector(x, y)  # position
        self.vel = Vector(0, 0)  # velocity
        self.acc = Vector(0, GRAVITY)  # acceleration

        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

        self.image = pg.Surface((self.w, self.h))
        self.image.fill(RED)
        # self.image = pg.image.load("../resources/player.*")

    def update(self):
        """
        I'm also a docstring hurr durr
        """
        # todo keylistener in seperate thread
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.moveLeft = True
        if keys[pg.K_RIGHT]:
            self.moveRight = True
        if keys[pg.K_SPACE]:
            self.jump = True

        # acceleration
        if self.moveLeft:
            print("left")
            self.acc.x = -ACCELERATION
            self.moveLeft = False
        if self.moveRight:
            print("right")
            self.acc.x = ACCELERATION
            self.moveRight = False
        if self.jump:
            self.vel.y = -10
            self.jump = False

        # resistance
        self.acc.x -= self.vel.x * FRICTION
        self.acc.y -= self.vel.y * FRICTION

        # update velocity and position
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        (self.x, self.y) = self.pos.get()  # brak

        print(self.x, self.y)

        # update hitbox
        self.rect.midbottom = self.pos.get()

        # collision

        pg.sprite.spritecollideany(self, get_map(), False)
