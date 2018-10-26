import pygame as pg
from game.settings import *
from game.player import *
from game.sprites import *
from game.map.map import *
from os import path


class Game:
    """ platformer game """
    def __init__(self):
        """ initialize game window """
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
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
        self.map_tiles = None
        self.level = None

    def load_data(self):
        """ load level times """
        with open(path.join(self.dir, RECORDS_FILE), 'w') as f:
            try:
                self.records = int(f.read())
            except IOError:
                self.records = 0

    def new(self, lives, level):
        """ start new game, player lives set """
        self.lives = lives
        self.level = level
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(WIDTH / 2, HEIGHT / 2, 30, 20)
        self.all_sprites.add(self.player)
        '''
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        '''
        self.map = Map(level)
        self.map_tiles = self.map.getTiles()
        for tile in self.map_tiles:
            # platform
            if tile.data == 0:
                p = Platform(tile.x, tile.y, TILESIZE, TILESIZE)
                self.platforms.add(p)
            self.all_sprites.add(p)
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
        if self.player.vel.y > 0:
            # check for collision between player and platforms
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
        # if player reaches sides of screen, move the rest the opposite way
        if self.player.rect.right > WIDTH * 2 / 3:
            # note: the max(.. , 2) is a fix for drifting platforms in the right direction
            self.player.x -= max(self.player.vel.x, 2)
            for plat in self.platforms:
                plat.rect.right -= max(self.player.vel.x, 2)
        elif self.player.rect.left < WIDTH / 3:
            self.player.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.right -= self.player.vel.x

        # check all die conditions
        if self.player.rect.top > HEIGHT:
            if self.lives > 1:
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

    def draw(self):
        """ game loop - drawing """
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text("Lives: " + str(self.lives), 24, BLACK, WIDTH / 2, 15)
        self.draw_text(self.timer_string, 24, BLACK, WIDTH / 2, HEIGHT - 35)
        # after drawing everything, update the screen
        pg.display.flip()

    def show_start_screen(self):
        """ game start screen """
        self.screen.fill(WHITE)
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
        self.screen.fill(WHITE)
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
        self.screen.blit(text_surface, text_rect)

    def update_timer_string(self):
        """ updates the timer string that will be drawn to the screen """
        total_seconds = self.frame_count / FPS
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milli_sec = (seconds % 1) * 1000
        self.timer_string = "Time: {:02d}:{:02d}:{:03d}".format(int(minutes), int(seconds), int(milli_sec))
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


g = Game()
g.show_start_screen()
while g.running:
    g.new(PLAYER_LIVES, LEVEL_1)
    g.show_go_screen()

pg.quit()