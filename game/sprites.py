import pygame as pg

import game
from game.map import colorMap
from settings import *

vec = pg.math.Vector2

SIZE = TILESIZE


class Player(pg.sprite.Sprite):
    """ Player sprite """

    def __init__(self, game, prop, start, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(colorMap.RED)
        self.rect = self.image.get_rect()
        self.rect.midleft = start
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.change = vec(0, 0)
        self.collision_streak = 0

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
        self.change = self.vel + 0.5 * self.acc
        old_x = self.rect.x

        self.collisions()

        self.game.shift_world(self.rect.x - old_x)

    def collisions(self):
        """ Check and handle collisions """

        # check if we glitched inside a platform. If so, increase collision streak
        self.rect.y -= TILESIZE / 4
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if hit.rect.collidepoint(self.rect.midbottom):
                    self.collision_streak += 1
                    if self.collision_streak > 5:
                        self.rect.bottom = hit.rect.top
        self.rect.y += TILESIZE / 4

        # normal collision handling
        self.rect.x += round(self.change.x)
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if self.change.x > 0:
                self.rect.right = hit.rect.left
                self.vel.x = 0
            elif self.change.x < 0:
                self.rect.left = hit.rect.right
                self.vel.x = 0

        self.rect.y += self.change.y
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit in hits:
            if self.change.y > 0:
                self.rect.bottom = hit.rect.top
                self.vel.y = 0
            elif self.change.y < 0:
                self.rect.top = hit.rect.bottom
                self.vel.y = 0


class Platform(pg.sprite.Sprite):
    """ Platform sprite """

    def __init__(self, x, y, w, h, c):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        if c is not None:
            self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pg.sprite.Sprite):
    """
    Enemy superclass. Contains all common enemy properties.
    """

    def __init__(self, x, y):
        super(Enemy, self).__init__()

        self.x = x
        self.y = y

    def update(self):
        print("WARNING: Enemy superclass should not be constructed.")
        self.kill()

    # todo collision with player


class Bee(Enemy):
    """
    Slow enemy that follows the player. Does not have collision
    """

    def __init__(self, x, y):
        super(Bee, self).__init__(x, y)

        # self.image = pg.image.load()
        self.image = pg.Surface((SIZE, SIZE))
        self.image.fill(pg.Color("white"))

        self.rect = self.image.get_rect()

    def update(self):
        if self.x > game.game.player.x:
            self.x -= 1
        else:
            self.x += 1
        if self.y > game.game.player.y:
            self.y -= 1
        else:
            self.y += 1
