import os
import pygame as pg


def getSound(sound):
    dirname = os.path.dirname(__file__)
    return pg.mixer.Sound(os.path.join(dirname, sound))
