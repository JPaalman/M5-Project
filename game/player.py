import pygame as pg

from settings import *
from utils import polarity, Vector

ACCELERATION = 1  # dummy value
FRICTION = 0  # dummy value
GRAVITY = 1  # dummy value
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
        self.acc.x -= self.vel.x * FRICTION * polarity(self.acc.x)
        self.acc.y -= self.vel.y * FRICTION * polarity(self.acc.x)

        # update velocity and position
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        (self.x, self.y) = self.pos.get()  # brak

        print(self.x, self.y)

        # update hitbox
        self.rect.topleft = self.pos.get()

        # collision
        self.collision()

    def collision(self):
        """
        I f*cking hate docstrings
        """
        # todo find a way to differentiate between vertical and horizontal collision
        # todo move the collision handling to the tiles and check for collision with all sprites
        from game.game import get_map
        tiles = get_map()
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = tile.rect.left
                    self.vel.x *= -0.5
                    self.acc.x = 0
                if self.vel.x < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = tile.rect.right
                    self.vel.x *= -0.5
                    self.acc.x = 0
                if self.vel.y > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = tile.rect.top
                    self.vel.y *= -0.5
                    self.acc.y = 0
                if self.vel.y < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = tile.rect.bottom
                    self.vel.y *= -0.5
                    self.acc.y = 0
