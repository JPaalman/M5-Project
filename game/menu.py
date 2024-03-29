import pygame as pg
from game import settings
from game.map import colorMap
from game.resources import resourceManager
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

        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = None
        pg.display.flip()

        self.highscores = resourceManager.getHighscores()

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
                    if event.key == pg.K_ESCAPE:
                        return -1
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
                if event.type == pg.QUIT:
                    return -1
            pg.event.pump()
            time.sleep(1/70)

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
                if event.type == pg.QUIT:
                    return False
            pg.event.pump()
            time.sleep(0.05)

    def displayHighscores(self, playlist, offset=0, color=colorMap.BLACK):
        """
        Displays the highscores of a playlist in a nice format
        :param playlist: name of the target playlist
        :param offset: vertical position of the highscores display
        """
        offset += 30
        count = 1

        try:
            scores = self.highscores[playlist]
        except KeyError:
            self.highscores[playlist] = []
            scores = self.highscores[playlist]

        if scores is None:
            self.draw_text("No highscores found", 30, color, settings.WIDTH / 2, (settings.HEIGHT / 2 + offset))
        else:
            self.draw_text("Highscores:", 30, color, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
            offset += 40
            for x in scores:
                self.draw_text(str(x), 30, color, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
                self.draw_text(str(count) + ": ", 30, color, (settings.WIDTH / 2 - (settings.TILESIZE * 8)), (settings.HEIGHT / 2 + offset))
                count += 1
                offset += 40

    def drawPlaylistName(self, index):
        """
        Displays the name of one of the playlists, and displays their respective highscores.
        :param index: the index where the playlist name is stored at.
        """
        self.display.blit(self.bg, (0, 0))
        self.selectedPlaylistName = settings.PLAYLIST[index][0]
        self.draw_text(self.selectedPlaylistName, 30, colorMap.WHITE, settings.WIDTH / 2,
                            settings.HEIGHT / 3)
        self.displayHighscores(settings.PLAYLIST[index][0], -100, colorMap.NAVYBLUE)
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

        place = -1

        if last:
            print("updating highscores")
            place = self.updateHighscores(gameTime, coins, playlistName)

        self.display.blit(self.fi, (0, 0))
        self.draw_text("Finish!", 80, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 - 150)
        if last:
            self.displayScoreCalculation(gameTime, coins)
            self.draw_text("Press [space] to continue, or press [esc] to quit", 25, colorMap.BLACK, settings.WIDTH / 2,
                           settings.HEIGHT / 2 + 125)
        else:
            self.draw_text("Press [space] to go to next level!", 30, colorMap.BLACK, settings.WIDTH / 2,
                           settings.HEIGHT / 2 + 50)

        pg.display.flip()

        """
        up = False
        while not up:
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    up = True
            pg.event.pump()
        """

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return False
                    if event.key == pg.K_SPACE:
                        if last:
                            self.display.blit(self.fi, (0,0))
                            if place != -1:
                                self.draw_text("You!", 30, colorMap.YELLOW, settings.WIDTH / 2 + 150, settings.HEIGHT / 2 - 10 + (place - 1) * 40)
                            self.draw_text("Finish!", 80, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 - 150)
                            self.displayHighscores(playlistName, -80,)
                            self.draw_text("Press [space] to continue, or press [esc] to quit", 25, colorMap.BLACK,
                                           settings.WIDTH / 2,
                                           settings.HEIGHT / 2 + 125)
                            pg.display.flip()
                            while True:
                                for event1 in pg.event.get():
                                    if event1.type == pg.KEYDOWN:
                                        if event1.key == pg.K_ESCAPE:
                                            return False
                                        if event1.key == pg.K_SPACE:
                                            return True
                                    if event1.type == pg.QUIT:
                                        return False
                                pg.event.pump()
                                time.sleep(0.1)
                        else:
                            return True
                if event.type == pg.QUIT:
                    return False
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
        self.draw_text("Coins bonus: " + str(coins) + " x " + str(settings.POINTS_PER_COIN), 30, colorMap.BLACK, settings.WIDTH / 2, settings.HEIGHT / 2 + offset)
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
        return settings.BASE_POINTS - time * settings.POINTS_LOSS_PER_SECOND

    def calculateCoinsBonus(self, coins):
        """
        Calculate how many points the player got by collecting coins
        :param coins: the amount of coins that the player collected
        :return: the amount of points gained by collecting coins
        """
        return coins * settings.POINTS_PER_COIN

    def updateHighscores(self, gametime, coins, playlist):
        score = self.calculateTimeScore(gametime) + self.calculateCoinsBonus(coins)
        print("score " + str(score))
        out = -1
        old = {}
        try:
            ls = self.highscores[playlist]
            old = ls
            print("initial values: " + str(ls))
            tmp = []

            for x in ls:
                tmp.append(int(x))
            ls = tmp

            ls.append(score)
            print("new scores " + str(ls))
            ls.sort(reverse=True)
            self.highscores[playlist] = ls
        except KeyError:
            print("keyerror")
            return

        res = []

        index = 0
        while index < len(self.highscores[playlist]) and index < 3:
            res.append(self.highscores[playlist][index])
            index += 1

        print(str(res))

        self.highscores[playlist] = res
        print(str(self.highscores[playlist]))
        resourceManager.writeHighscores(self.highscores)

        if old != res:
            index = len(res) - 1
            while index > 0 and res[index] != score:
                index -= 1
            out = index + 1

        return out