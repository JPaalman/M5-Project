import pygame as pg
from game.map import colorMap
from game.settings import *
import game.resources.resourceManager as rM
import time

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """ Player sprite """

    def __init__(self, game, prop, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(colorMap.RED)
        self.rect = self.image.get_rect()
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

    def set_start(self, start):
        """ Sets player start position """
        self.rect.midleft = start

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
                    if self.collision_streak > 2:
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

        # first check whether the player is standing on a jump-pad
        hits = pg.sprite.spritecollide(self, self.game.jump_pads, False)
        jmp = False
        for hit in hits:
            if (self.rect.collidepoint(hit.rect.midtop)
                    or self.rect.collidepoint(hit.rect.topright)
                    or self.rect.collidepoint(hit.rect.topleft)):
                self.rect.bottom = hit.rect.top  # put player on top of jump pad first
                jmp = True
                self.vel.y *= -1.2
                break

        if not jmp:
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

    def __init__(self, x, y, tile_id, width):
        pg.sprite.Sprite.__init__(self)

        if width is None:
            width = 1

        self.image = pg.Surface((TILESIZE * width, TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id)
        else:
            c = colorMap.colours[tile_id]
            if c is not None:
                self.image.fill(c)
            else:
                self.image.fill(colorMap.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingPlatform(pg.sprite.Sprite):
    """ Moving platform sprite """
    def __init__(self, game, x, y, tile_id, width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE * width, TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id)
        else:
            c = colorMap.colours[tile_id]
            if c is not None:
                self.image.fill(c)
            else:
                self.image.fill(colorMap.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.speed = game.map.PLATFORM_SPEED
        self.direction = -1  # 1 is forward, -1 is backwards

    def update(self):
        """ Handles the movement """
        self.rect.x += self.speed * self.direction
        if self.rect.collidepoint(self.game.player.rect.midbottom):
            self.game.player.rect.x += self.speed * self.direction

        shift = TILESIZE * self.direction
        self.rect.left += shift
        if self.rect.colliderect(self.game.player.rect):
            self.direction *= -1
        self.rect.left -= shift

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.handle_hits(hits)
        hits = pg.sprite.spritecollide(self, self.game.ai_borders, False)
        self.handle_hits(hits)

    def handle_hits(self, hits):
        """ Handles collision of moving platforms """
        if hits:
            for hit in hits:
                if hit.rect != self.rect:
                    if hit.rect.collidepoint(self.rect.midright):
                        self.rect.right = hit.rect.left
                    if hit.rect.collidepoint(self.rect.midleft):
                        self.rect.left = hit.rect.right
                    self.direction *= -1


class GroundCrawler(pg.sprite.Sprite):
    """ Enemy sprite"""

    def __init__(self, game, x, y, tile_id, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id)
        else:
            c = colorMap.colours[tile_id]
            if c is not None:
                self.image.fill(c)
            else:
                self.image.fill(colorMap.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.speed = speed
        self.direction = 1  # 1 is forward, -1 is backwards

    def update(self):
        """ Handles the movement """
        self.rect.x += self.speed * self.direction
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.handle_hits(hits)
        hits = pg.sprite.spritecollide(self, self.game.ai_borders, False)
        self.handle_hits(hits)
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        self.handle_hits(hits)

    def handle_hits(self, hits):
        """ When the enemy collides with something, turn its direction the other way """
        if hits:
            for hit in hits:
                if hit.rect is not self.rect:
                    if hit.rect.collidepoint(self.rect.midright):
                        self.rect.right = hit.rect.left
                    if hit.rect.collidepoint(self.rect.midleft):
                        self.rect.left = hit.rect.right
                    self.direction *= -1



class Laser(pg.sprite.Sprite):
    """Laser of death"""

    def __init__(self, game, x, y, tile_id):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id)
        else:
            c = colorMap.colours[tile_id]
            if c is not None:
                self.image.fill(c)
            else:
                self.image.fill(colorMap.BLACK)

        self.img = rM.getImageById(33)
        self.texture = rM.getImageById(256)
        self.tid = tile_id

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.on = False
        self.timer = time.time()
        self.beam = Beam(x, y)

        self.game.all_sprites.add(self.beam)

    def update(self):
        #print(str(time.time()))
        #print(str(self.timer))
        #print(" ")
        if self.on and (time.time() - self.timer > 1):
            print("turning off laser")
            self.on = False
            self.game.death_tiles.remove(self.beam)
            self.beam.image = pg.Surface((TILESIZE, 1000), pg.SRCALPHA, 32)
            self.beam.image.convert_alpha()
            self.timer = time.time()
        elif not self.on and (time.time() - self.timer > 1):
            print("turning on laser")
            self.on = True
            self.beam.image.fill(colorMap.RED)
            self.game.death_tiles.add(self.beam)
            self.timer = time.time()


class Beam(pg.sprite.Sprite):

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE, 1000), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 1000

    def update(self):
        1