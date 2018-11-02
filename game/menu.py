import pygame as pg
from game import settings
from game.map import colorMap
from game.resources import resourceManager
from game import utils
import time


class Menu:

    def __init__(self, display):
        self.font_name = pg.font.match_font(settings.FONT_NAME)
        self.display = display
        # TODO put bg image path in settings.py
        self.bg = resourceManager.getImage("main_menu.png", False)
        self.display.blit(self.bg, (0, 0))
        utils.draw_text(self.display, self.font_name, "fake mario", 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2.5)
        pg.display.flip()

    def selectMap(self):
        print("woop")