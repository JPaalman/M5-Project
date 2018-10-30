import pygame as pg

from game.settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """ Player sprite """

    def __init__(self, game, prop, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.PLAYER_WIDTH = w
        self.PLAYER_HEIGHT = h
        self.PLAYER_ACC = prop[0]
        self.PLAYER_FRICTION = prop[1]
        self.PLAYER_GRAV = prop[2]
        self.PLAYER_JUMP = prop[3]

    def jump(self):
        """ Makes the player jump """
        # jump only if we are on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -self.PLAYER_JUMP

    def update(self):
        """ Updates the player's acceleration / velocity / etc """
        self.acc = vec(0, self.PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -self.PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = self.PLAYER_ACC

        self.acc.x += self.vel.x * -self.PLAYER_FRICTION
        self.vel += self.acc
        change = self.vel + 0.5 * self.acc
        old_x = self.rect.x

        # Check and handle collisions
        self.rect.x += change.x
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if change.x > 0:
                self.rect.right = hit.rect.left
                self.vel.x = 0
            elif change.x < 0:
                self.rect.left = hit.rect.right
                self.vel.x = 0

        self.rect.y += change.y
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if change.y > 0:
                self.rect.bottom = hit.rect.top
                self.vel.y = 0
            elif change.y < 0:
                self.rect.top = hit.rect.bottom
                self.vel.y = 0

        self.game.shift_world(self.rect.x - old_x)


class Platform(pg.sprite.Sprite):
    """ Platform sprite """
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
