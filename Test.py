from game.menu import Menu
import pygame as pg
from game import settings
import time

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))  # (0, pg.FULLSCREEN)[FULLSCREEN]
pg.display.set_caption(settings.TITLE)

Menu(screen)
time.sleep(5)