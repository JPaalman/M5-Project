import pygame as pg
from game.map import colorMap
import resources.resourceManager as resourceManager


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

        self.imgSurface = self.setTexture()

    def setTexture(self):
        if self.tile_id in colorMap.uses_texture:
            return resourceManager.getImageById(self.tile_id)
        return None
