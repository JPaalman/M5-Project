import pygame as pg
from game import settings
from game.map import colorMap
from game.resources import resourceManager
import os
import time


class Menu:
    """
        This class manages the displays inbetween playing the game, like selecting a map,
        gameover screen and finish screen.
    """
    def __init__(self, display):
        self.font_name = pg.font.match_font(settings.FONT_NAME)
        self.display = display

        self.bg = resourceManager.getImage(settings.main_menu_image, False)
        self.go = resourceManager.getImage(settings.game_over_image, False)
        self.fi = resourceManager.getImage(settings.finish_image, False)

        self.pointsPerCoin = 500

        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = None
        pg.display.flip()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, settings.highscores_file)
        file_object = open(filename, )
        self.highscores = self.initHighScores(file_object.readlines())

    def selectPlaylist(self):
        """
        Displays the menu for selecting a playlist. The user can cycle through the playlist names and their highscores.
        :return: The name of the playlist that the user wants to play.
        """
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
                        return index
            pg.event.pump()
            time.sleep(0.05)

    def gameOver(self):
        """
        Displays the gameover screen giving the user the option to either play again or quit
        :return: True if play again, False if quit
        """
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

    def displayHighscores(self, playlist, offset=0):
        """
        Displays the highscores of a playlist in a nice format
        :param playlist: name of the target playlist
        :param offset: vertical position of the highscores display
        """
        offset += 30
        count = 1

        scores = self.highscores[playlist]
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
        """
        Retrieves all highscores from the highscores.txt file and puts them into a Dictionary for the class to use
        later on.
        :param lines: The raw lines of the highscores.txt file
        :return: the dictionary containing all highscores for all playlists.
        """
        mp = {}

        for x in lines:
            tmp = x.split("=")
            scores = []
            for y in tmp[1].split(","):
                scores.append(int(y))
            mp[tmp[0]] = scores

        return mp

    def drawPlaylistName(self, index):
        """
        Displays the name of one of the playlists, and displays their respective highscores.
        :param index: the index where the playlist name is stored at.
        """
        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = settings.PLAYLIST[index][0]
        self.draw_text(self.selectedPlaylistName, 30, colorMap.BLACK, settings.WIDTH / 2,
                        settings.HEIGHT / 2.3)
        self.displayHighscores(settings.PLAYLIST[index][0],)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        """ draw text to the screen at position x, y """
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.display.blit(text_surface, text_rect)

    def finish(self, last, playlistName, gameTime, coins):
        """
        Displays the finish screen showing the end score, the calculation of it and the highscores for this playlist.
        The user can either continue and play again or quit
        :param playlistName: name of the played playlist
        :param gameTime: time in which the player finished the playllist
        :param coins: the amount of coins that the player collected
        :return: True if the player wants to play again, False if the player wants to quit.
        """
        self.display.blit(self.fi, (0, 0))
        self.draw_text("Finish!", 80, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 - 150)
        if last:
            self.displayScoreCalculation(gameTime, coins)
        self.draw_text("Press [space] to continue, or press [esc] to quit", 25, colorMap.BLACK, settings.WIDTH / 2,
                       settings.HEIGHT / 2 + 125)
        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        return False
                    if event.key == pg.K_SPACE:
                        if last:
                            self.display.blit(self.fi, (0,0))
                            self.draw_text("Finish!", 80, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 - 150)
                            self.displayHighscores(playlistName, -80)
                            self.draw_text("Press [space] to continue, or press [esc] to quit", 25, colorMap.BLACK,
                                           settings.WIDTH / 2,
                                           settings.HEIGHT / 2 + 125)
                            pg.display.flip()
                            while True:
                                for event1 in pg.event.get():
                                    if event1.type == pg.KEYUP:
                                        if event1.key == pg.K_ESCAPE:
                                            return False
                                        if event1.key == pg.K_SPACE:
                                            return True
                                pg.event.pump()
                                time.sleep(0.1)
                        else:
                            return True
            pg.event.pump()
            time.sleep(0.1)

    def displayScoreCalculation(self, gameTime, coins):
        """
        Shows a formatted display of the score and how it was calculated
        :param gameTime: the amount of time that the player needed to finish the playlist
        :param coins: the amount of coins that the player collected
        """
        offset = -50
        self.draw_text("Time score: " + str(self.calculateTimeScore(gameTime)), 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
        offset += 35
        self.draw_text("Coins bonus: " + str(coins) + " x " + str(self.pointsPerCoin), 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
        offset += 10
        self.draw_text("____________________", 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
        offset += 35
        self.draw_text("Score: " + str(self.calculateTimeScore(gameTime) + self.calculateCoinsBonus(coins)), 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)

    def calculateTimeScore(self, time):
        """
        Calculate the score based on time
        :param time: playtime
        :return: the score from time
        """
        return time * 50

    def calculateCoinsBonus(self, coins):
        """
        Calculate how many points the player got by collecting coins
        :param coins: the amount of coins that the player collected
        :return: the amount of points gained by collecting coins
        """
        return coins * self.pointsPerCoin
