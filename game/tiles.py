import pygame as pg

class Tile(pg.sprite.Sprite):
    """
    instance variables:
    x (x-coordinate top left of tile)
    y (y-coordinate top left of tile)
    w (width)
    h (height
    texturePath (path to texture)
    rect (hitbox for collision)

    bytemap:
    32 = nothing
     = tile

    """

    def __init__(self, x, y, tile_id, data):
        super().__init__()

        self.x = x
        self.y = y
        self.tile_id = tile_id
        self.data = data
