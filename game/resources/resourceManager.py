import os
import pygame as pg

dirname = os.path.dirname(__file__)

texturemap = {
    33: "transparent.png",
    68: "lava.png",
    69: "android.png",
    112: "finish_flag.png",
    67: "flag.png",
    61: "gras-ground2.png",
    70: "ground2.png",
    99: "coin.png",
    45: "platform-middle.png",
    83: "spike.png"
}

uses_alpha = {33, 69, 112, 67, 99, 83}


def getImageById(imgid):
    if imgid in texturemap:
        return getImage(texturemap[imgid], imgid in uses_alpha)
    else:
        print("TRANSPARENT: " + str(imgid))
        return getImage("transparent.png", True)


def getImage(imgstr, alpha):
    img = pg.image.load(os.path.join(dirname, imgstr))
    if alpha:
        return img.convert_alpha()
    else:
        return img.convert()
