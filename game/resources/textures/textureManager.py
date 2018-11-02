import os
import pygame as pg


def getImage(imgstr, alpha):
    dirname = os.path.dirname(__file__)
    img = pg.image.load(os.path.join(dirname, imgstr))
    if alpha:
        return img.convert_alpha()
    else:
        return img.convert()