import pygame as pg

from game.settings import TILESIZE


class Tile(pg.sprite.Sprite):
    '''
    instance variables:
    x (x-coordinate top left of tile)
    y (y-coordinate top left of tile)
    w (width)
    h (height
    texturePath (path to texture)
    rect (hitbox for collision)
    '''

    def __init__(self, new_x, new_y, new_byte, new_data):
        super().__init__()
        self.x = new_x
        self.y = new_y
        self.byte = new_byte
        self.data = new_data
        if self.data != 0:
            self.byte = 64
        # self.texturePath = self.setTexture()
        self.rect = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)

    def setTexture(self):
        return ""
        # TODO select texture based on byte
