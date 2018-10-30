from os import path

import pygame as pg
from pygame.locals import *

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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.fake_screen = self.screen.copy()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.display.set_caption(TITLE)
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

        self.dir = path.dirname(__file__)
        self.records = None
        self.load_data()
        self.lives = None
        self.all_sprites = None
        self.sprites_on_screen = None
        self.platforms = None
        self.player = None
        self.playing = None
        self.frame_count = None
        self.timer_string = None
        self.map = None
        self.level = None

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
            # platform
            if t.byte == 71:
                p = Platform(t.x, t.y, TILESIZE, TILESIZE)
                self.platforms.add(p)
            self.all_sprites.add(p)

    def new(self, lives, level):
        """ start new game, player lives set """
        self.lives = lives
        self.level = level
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
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
        self.player = Player(self, player_properties,
                             WIDTH / 2, HEIGHT / 2,
                             TILESIZE, TILESIZE * 3 / 2)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        """ game loop """
        self.frame_count = 0
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """ update all the things! """
        # update timer
        self.update_timer_string()
        # game loop updates
        self.all_sprites.update()

        # check all die conditions
        if self.player.rect.top > HEIGHT:
            if self.lives > 1:
                print(self.lives)
                self.new(self.lives - 1, self.level)
            else:
                self.playing = False
        # todo: killed by enemy

    def events(self):
        """ game loop - handling events """
        for event in pg.event.get():
            # check for close window event
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            elif event.type == VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.dict['size']

    def draw(self):
        """ game loop - drawing """
        self.fake_screen.fill(WHITE)
        self.all_sprites.draw(self.fake_screen)
        self.draw_text("Lives: " + str(self.lives), 24, BLACK, WIDTH / 2, 15)
        self.draw_text(self.timer_string, 24, BLACK, WIDTH / 2, HEIGHT - 35)
        # after drawing everything, update the screen with the fake surface
        screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.blit(pg.transform.scale(self.fake_screen, (self.WIDTH, self.HEIGHT)), (0, 0))
        pg.display.flip()

    def show_start_screen(self):
        """ game start screen """
        self.fake_screen.fill(WHITE)
        self.draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        # todo: display record times for each level...
        self.draw_text("Record time: " + str(self.records), 22, BLACK, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        """ if game is closed mid game, skip the game over screen """
        if not self.running:
            return

        # game over / continue
        self.fake_screen.fill(WHITE)
        self.draw_text("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)

        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        """ draw text to the screen at position x, y """
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.fake_screen.blit(text_surface, text_rect)

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
        if self.player.rect.right > WIDTH * 2 / 3:
            self.player.rect.x -= shift_x
            for plat in self.platforms:
                plat.rect.right -= shift_x
        elif self.player.rect.left < WIDTH / 3:
            self.player.rect.x -= shift_x
            for plat in self.platforms:
                plat.rect.right -= shift_x

g = Game()
g.show_start_screen()
while g.running:
    g.new(PLAYER_LIVES, LEVEL_1)
    g.show_go_screen()

pg.quit()
