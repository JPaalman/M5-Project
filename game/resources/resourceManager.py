import os
import pygame as pg

dirname = os.path.dirname(__file__)

texturemap = {
    33: "transparent.png",
    68: "lava.png"
}


def getImageById(imgid):
    if imgid in texturemap:
        return getImage(texturemap[imgid])
    else:
        return getImage("transparent.png")


def getImage(imgstr):
    img = pg.image.load(os.path.join(dirname, imgstr))
    return img.convert()
