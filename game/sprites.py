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
        self.image = rM.getImage("idle.gif", True)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.change = vec(0, 0)
        self.collision_streak = 0

        # properties
        self.PLAYER_WIDTH = w
        self.PLAYER_HEIGHT = h
        self.PLAYER_ACC = prop[0]
        self.PLAYER_FRICTION = prop[1]
        self.PLAYER_GRAV = prop[2]
        self.PLAYER_JUMP = prop[3]

        # sounds
        self.jump_pad_sound = rM.getSound("Trampoline2.wav")

        # animations
        self.IDLE_IMAGE_RIGHT = rM.getImage("idle.gif", True)
        self.JUMP_IMAGE_RIGHT = rM.getImage("jump.png", True)
        self.FALL_IMAGE_RIGHT = rM.getImage("mid air.gif", True)

        self.IDLE_IMAGE_LEFT = rM.getImage("idle_inverted.gif", True)
        self.JUMP_IMAGE_LEFT = rM.getImage("jump_inverted.png", True)
        self.FALL_IMAGE_LEFT = rM.getImage("mid air_inverted.gif", True)

        self.last_direction_right = True

        images = []
        for n in range(0, 8):
            images.append(rM.getImage("character_run" + str(n) + ".gif", True))
        self.runanimationright = TextureCycler(self, images, 0.07)

        images = []
        for n in range(0, 8):
            images.append(rM.getImage("character_run" + str(n) + "_inverted.gif", True))
        self.runanimationleft = TextureCycler(self, images, 0.07)

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

        # Handle player animations
        if self.vel.x < -0.5:
            self.last_direction_right = False
            if self.vel.y > 0.5:
                self.image = self.JUMP_IMAGE_LEFT
            elif self.vel.y < -0.5:
                self.image = self.FALL_IMAGE_LEFT
            else:
                self.runanimationleft.tick()
        elif self.vel.x > 0.5:
            self.last_direction_right = True
            if self.vel.y > 0.5:
                self.image = self.JUMP_IMAGE_RIGHT
            elif self.vel.y < -0.5:
                self.image = self.FALL_IMAGE_RIGHT
            else:
                self.runanimationright.tick()
        elif self.last_direction_right:
            self.image = self.IDLE_IMAGE_RIGHT
        else:
            self.image = self.IDLE_IMAGE_LEFT

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
                pg.mixer.Sound.play(self.jump_pad_sound)
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

    def __init__(self, x, y, tile_id, width, style):
        pg.sprite.Sprite.__init__(self)

        if width is None:
            width = 1

        self.image = pg.Surface((TILESIZE * width, TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id, style)
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
            shift_x = self.speed * self.direction
            self.game.shift_world(shift_x)
            self.game.player.rect.x += shift_x

        shift = TILESIZE * self.direction * 0.5
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

    def __init__(self, game, x, y, tile_id, speed, style):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        if tile_id in colorMap.uses_image:
            self.image = rM.getImageById(tile_id, style)
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


class Ghost(pg.sprite.Sprite):
    """ Enemy sprite"""

    def __init__(self, game, x, y, tile_id, speed, style):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = rM.getImage("ghost0.png", True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 6
        self.game = game
        self.speed = speed
        self.direction = 1  # 1 is forward, -1 is backwards

        images = []
        for n in range(0, 3):
            images.append(rM.getImage("ghost" + str(n) + ".png", True))
        images.append(rM.getImage("ghost1.png", True))
        self.runanimationright = TextureCycler(self, images, 0.5)

        images = []
        for n in range(0, 3):
            images.append(rM.getImage("ghost" + str(n) + "_inverted.png", True))
        images.append(rM.getImage("ghost1_inverted.png", True))
        self.runanimationleft = TextureCycler(self, images, 0.5)

    def update(self):
        """ Handles the movement """
        self.rect.x += self.speed * self.direction
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.handle_hits(hits)
        hits = pg.sprite.spritecollide(self, self.game.ai_borders, False)
        self.handle_hits(hits)
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        self.handle_hits(hits)

        if self.direction == 1:
            self.runanimationright.tick()
        else:
            self.runanimationleft.tick()

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
                    return


class Laser(pg.sprite.Sprite):
    """Laser of death"""

    def __init__(self, game, x, y, tile_id):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.tid = tile_id

        self.images = []
        for n in range(0, 5):
            self.images.append(rM.getImage("laser" + str(n) + ".png", False))
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.on = False
        self.timer = time.time()
        self.beam = Beam(x, y)

        self.state = 0
        self.game.all_sprites.add(self.beam)

    def update(self):
        dt = time.time() - self.timer
        if dt > LASER_DOWNITME / 4 and self.state != 4:
            self.state += 1
            self.image = self.images[self.state]
            if self.state == 4:
                self.game.death_tiles.add(self.beam)
                self.beam.image.fill(colorMap.RED)
            self.timer = time.time()

        if self.state == 4 and dt > LASER_UPTIME:
            self.state = 0
            self.image = self.images[self.state]
            self.game.death_tiles.remove(self.beam)
            self.beam.image = pg.Surface((TILESIZE - (2 * self.beam.margin), 1000), pg.SRCALPHA, 32)
            self.beam.image.convert_alpha()
            self.timer = time.time()


class Beam(pg.sprite.Sprite):

    margin = 2

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((TILESIZE - (2 * self.margin), 1000), pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x + self.margin
        self.rect.y = y - 1000


class TextureCycler():

    def __init__(self, sprite, images, tickrate):
        self.sprite = sprite
        self.images = images
        self.timer = time.time()
        self.tickrate = tickrate
        self.index = 0

    def tick(self):
        dt = time.time() - self.timer
        if dt > self.tickrate:
            self.index += 1
            if self.index == len(self.images):
                self.index = 0
            self.sprite.image = self.images[self.index]
            self.timer = time.time()

