import os
import pygame as pg

dirname = os.path.dirname(__file__)

texturemap = {
    33: "transparent.png"
}


def getImageById(imgid):
    return getImage(texturemap[imgid])


def getImage(imgstr):
    img = pg.image.load(os.path.join(dirname, imgstr))
    return img.convert()
