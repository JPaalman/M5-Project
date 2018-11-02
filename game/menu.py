import pygame as pg
from game import settings
from game.map import colorMap
from game.resources import resourceManager
import os
import time


class Menu:

    def __init__(self, display):
        self.font_name = pg.font.match_font(settings.FONT_NAME)
        self.display = display
        self.bg = resourceManager.getImage(settings.main_menu_image, False)
        self.go = resourceManager.getImage(settings.game_over_image, False)
        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = None
        pg.display.flip()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, settings.highscores_file)
        file_object = open(filename, )
        self.highscores = self.initHighScores(file_object.readlines())

    def selectMap(self):
        index = 0
        self.drawPlaylistName(index)
        while True:
            right = True
            left = True

            for event in pg.event.get():
                # test events, set key states
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and left:
                        left = False
                        index -= 1
                        if index < 0:
                            index = len(settings.PLAYLIST) - 1
                        self.drawPlaylistName(index)
                    if event.key == pg.K_RIGHT and right:
                        right = False
                        index += 1
                        if index == len(settings.PLAYLIST):
                            index = 0
                        self.drawPlaylistName(index)
                    if event.key == pg.K_SPACE:
                        print("selected: " + self.selectedPlaylistName)
                        return settings.PLAYLIST[index]
            pg.event.pump()
            time.sleep(0.05)

    def gameOver(self):
        self.display.blit(self.go, (0, 0))
        self.draw_text("GAME OVER", 80, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 - 60)
        self.draw_text("Press [space] to play again, or press [esc] to quit", 25, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + 40)
        pg.display.flip()

        while True:
            for event in pg.event.get():
                # test events, set key states
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    if event.key == pg.K_SPACE:
                        while True:
                            pg.event.pump()
                            for event1 in pg.event.get():
                                if event1.type == pg.KEYUP and event1.key == pg.K_SPACE:
                                    return True
                            time.sleep(0.05)
            pg.event.pump()
            time.sleep(0.05)


    def displayHighscores(self, mapname):
        offset = 30
        count = 1

        scores = self.highscores[mapname]
        if scores is None:
            self.draw_text("No highscores found", 30, colorMap.BLACK, settings.WIDTH / 2, (settings.HEIGHT / 2 + offset))
        else:
            self.draw_text("Highscores:", 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
            offset += 40
            for x in scores:
                self.draw_text(str(x), 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
                self.draw_text(str(count) + ": ", 30, colorMap.BLACK, (settings.WIDTH / 2 - (settings.TILESIZE * 8)), (settings.HEIGHT / 2 + offset))
                count += 1
                offset += 40


    def initHighScores(self, lines):
        mp = {}

        for x in lines:
            tmp = x.split("=")
            scores = []
            for y in tmp[1].split(","):
                scores.append(int(y))
            mp[tmp[0]] = scores

        return mp

    def drawPlaylistName(self, index):
        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = settings.PLAYLIST[index][0]
        self.draw_text(self.selectedPlaylistName, 30, colorMap.BLACK, settings.WIDTH / 2,
                        settings.HEIGHT / 2.3)
        self.displayHighscores(settings.PLAYLIST[index][0])
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        """ draw text to the screen at position x, y """
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.display.blit(text_surface, text_rect)