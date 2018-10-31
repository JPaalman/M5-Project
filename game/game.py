from os import path
from threading import Thread

import pygame as pg

from game.map import colorMap
from map.map import Map
from settings import *
from sprites import Platform
from sprites import Player


class Game:
    """ platformer game """

    def __init__(self):
        """ initialize game window """
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        if FULLSCREEN:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        self.bg = pg.image.load(bgImage)
        self.bg.convert()

        self.dir = path.dirname(__file__)
        self.records = None
        self.load_data()
        self.lives = None

        # init sprites
        self.all_sprites = None
        self.sprites_on_screen = None
        self.platforms = None
        self.player = None
        self.death_tiles = None

        self.playing = None
        self.frame_count = None
        self.timer_string = None
        self.map = None
        self.level = None
        self.player_start = None
        self.thread = None

        self.finish = None
        self.checkpoint = None

    def load_data(self):
        """ load level times """
        with open(path.join(self.dir, RECORDS_FILE), 'w') as f:
            try:
                self.records = int(f.read())
            except IOError:
                self.records = 0

    def init_map(self, map_tiles):
        """ Initialized all sprites from the level """
        for t in map_tiles:
            # player
            if t.tile_id == 80:
                self.player_start = (t.x, t.y)
            # finish
            elif t.tile_id == 112:
                f = Platform(t.x, t.y, TILESIZE, TILESIZE, colorMap.colours[t.tile_id])
                self.finish = f
                self.all_sprites.add(f)
            # AI border
            elif t.tile_id == 124:
                print("ADD ENEMIES!")
            # death tile
            elif t.tile_id in colorMap.death_tiles:
                d = Platform(t.x, t.y, TILESIZE, TILESIZE, colorMap.colours[t.tile_id])
                self.death_tiles.add(d)
                self.all_sprites.add(d)
            # the rest is assumed to be a platforms
            else:
                p = Platform(t.x, t.y, TILESIZE, TILESIZE, colorMap.colours[t.tile_id])
                self.platforms.add(p)
                self.all_sprites.add(p)

    def new(self, lives, level):
        """ start new game, player lives set """
        self.lives = lives
        self.level = level
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.death_tiles = pg.sprite.Group()
        '''
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        '''
        self.map = Map(level)
        self.init_map(self.map.getTiles())
        # player_properties = self.map.getPlayerProp()
        '''[PLAYER_ACC, PLAYER_FRICTION, PLAYER_GRAV, PLAYER_JUMP]'''
        player_properties = [1, 0.1, 0.8, 15]

        # if player has not reached a checkpoint, place on starting position
        if self.checkpoint is None:
            if self.player_start is None:
                self.player_start = (WIDTH / 2, HEIGHT / 2)
        else:
            self.player_start = self.checkpoint

        self.player = Player(self, player_properties,
                             self.player_start,
                             TILESIZE, TILESIZE * 3 / 2)
        self.all_sprites.add(self.player)

        thread = Thread(target=self.run())
        thread.start()

    def run(self):
        """ game loop """
        self.frame_count = 0
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        """ update all the things! """
        # update timer
        self.update_timer_string()
        # game loop updates
        self.all_sprites.update()

        # check all die conditions
        if (self.player.rect.top > HEIGHT or
                pg.sprite.spritecollide(self.player, self.death_tiles, False)):
            # start level again if you have enough lives left, otherwise stop playing
            if self.lives > 1:
                self.new(self.lives - 1, self.level)
            else:
                self.playing = False

        # check win conditions
        if self.player.rect.colliderect(self.finish.rect):
            self.playing = False

    def events(self):
        """ game loop - handling events """
        for event in pg.event.get():
            # check for close window event
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.key == pg.K_SPACE:
                    self.player.jump()

    def quit(self):
        """ stops the game """
        if self.playing:
            self.playing = False
        self.running = False

    def draw(self):
        """ game loop - drawing """
        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text("Lives: " + str(self.lives), 24, colorMap.BLACK, WIDTH / 2, 15)
        self.draw_text(self.timer_string, 24, colorMap.BLACK, WIDTH / 2, HEIGHT - 35)
        # after drawing everything, update the screen
        pg.display.flip()

    def show_start_screen(self):
        """ game start screen """
        self.screen.fill(colorMap.WHITE)
        self.draw_text(TITLE, 48, colorMap.BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, colorMap.BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        # todo: display record times for each level...
        self.draw_text("Record time: " + str(self.records), 22, colorMap.BLACK, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """ if game is closed mid game, skip the game over screen """
        if not self.running:
            return

        # game over / continue
        self.screen.fill(colorMap.WHITE)
        self.draw_text("GAME OVER", 48, colorMap.BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, colorMap.BLACK, WIDTH / 2, HEIGHT * 3 / 4)

        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        """ draw text to the screen at position x, y """
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update_timer_string(self):
        """ updates the timer string that will be drawn to the screen """
        if self.frame_count % FPS == 0:
            total_seconds = self.frame_count / FPS
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            ''' Measuring in ms causes too much lag, so we don't check this until run is completed '''
            # milli_sec = (seconds % 1) * 1000
            # self.timer_string = "Time: {:02d}:{:02d}:{:03d}".format(int(minutes), int(seconds), int(milli_sec))
            self.timer_string = "Time: {:02d}:{:02d}".format(int(minutes), int(seconds))
        self.frame_count += 1

    def wait_for_key(self):
        """ method that waits for a full button press (down and up) """
        waiting = True
        key_down = False
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    key_down = True
                if key_down and event.type == pg.KEYUP:
                    waiting = False

    def shift_world(self, shift_x):
        """ shift everything opposite of the change in x of the player """
        if self.player.rect.right > WIDTH * 2 / 3 and shift_x > 0:
            for sprite in self.all_sprites:
                sprite.rect.right -= shift_x
        elif self.player.rect.left < WIDTH / 3 and shift_x < 0:
            for sprite in self.all_sprites:
                sprite.rect.left -= shift_x


g = Game()
g.show_start_screen()
while g.running:
    g.new(PLAYER_LIVES, LEVEL_1)
    g.show_go_screen()

pg.quit()
