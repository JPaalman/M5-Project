import os
import pygame as pg


def getSound(sound):
    dirname = os.path.dirname(__file__)
    return pg.mixer.Sound(os.path.join(dirname, sound))

def loadMusic(sound):
    dirname = os.path.dirname(__file__)
    pg.mixer.music.load(os.path.join(dirname, sound))
