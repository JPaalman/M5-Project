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
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.PLAYER_ACC = prop[1]
        self.PLAYER_FRICTION = prop[2]
        self.PLAYER_GRAV = prop[3]
        self.PLAYER_JUMP = prop[4]

    def jump(self):
        """ Makes the player jump """
        # jump only if we are on a platform
        self.rect.y -= 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y += 1
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
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        # collision handling
        self.collision()

    def collision(self):
        """ Checks for collision with a platform """
        if self.vel.y > 0:
            # check for collision between player and platforms
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0



class Platform(pg.sprite.Sprite):
    """ Platform sprite """
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
