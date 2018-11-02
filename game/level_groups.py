import pygame as pg


class Level:
    """ Stores all sprites of a level """
    def __init__(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.death_tiles = pg.sprite.Group()
        self.checkpoints = pg.sprite.Group()
        self.ai_borders = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.sprites_on_screen = pg.sprite.Group()
        self.jump_pads = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.finishes = pg.sprite.Group()