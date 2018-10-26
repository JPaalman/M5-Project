import pygame as pg

from game.settings import *
from game.tiles import tile
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """
    I'm a docstring hurr durr
    """
    ACCELERATION = 60 / FPS  # dummy value
    FRICTION = 1  # dummy value
    GRAVITY = 1  # dummy value
    LIFE = 5

    def __init__(self, x, y, h, w):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((w, h))
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.x = x  # horizontal position
        self.y = y  # vertical position
        self.w = w  # width
        self.h = h  # height

        self.rect.center = (x, y)

        self.vel = vec(0, 0)  # velocity
        self.acc = vec(0, 0)  # acceleration

        # self.image = pg.image.load("../resources/player.*")

    def update(self):
        """
        I'm also a docstring hurr durr
        """
        # todo keylistener in seperate thread
        self.acc = vec(0, self.GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = self.ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acc.x = self.ACCELERATION
        if keys[pg.K_SPACE]:
            self.vel.y = -20

        self.acc.x -= self.vel.x * self.FRICTION

        self.vel.x += self.acc.x
        self.vel.y += self.acc.y

        self.x += self.vel.x + 0.5 * self.acc.x
        self.y += self.vel.y + 0.5 * self.acc.y

        self.rect.midbottom = vec(self.x, self.y )
        # self.collision()

    def collision(self):
        """
        I f*cking hate docstrings
        """
        # todo find a way to differentiate between vertical and horizontal collision
        # todo move the collision handling to the tiles and check for collision with all sprites
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
