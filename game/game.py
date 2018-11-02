from os import path
from threading import Thread
import pygame as pg
from game.level_groups import Level
from game.map import colorMap
from game.map.map import Map
from game.settings import *
from game.sprites import *
import game.resources.resourceManager as rM


class Game:
    """ platformer game """

    # Initialization of game
    def __init__(self):
        """ initialize game window """
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # (0, pg.FULLSCREEN)[FULLSCREEN]
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.playing = True
        self.has_won = False
        self.lives = PLAYER_LIVES
        self.coin_counter = 0

        # background
        self.bg = rM.getImage("bg.jpg", False)

        # level records
        self.dir = path.dirname(__file__)
        self.load_data()
        self.high_score = None

        # init sprite Groups
        self.level_groups = None
        self.player = None

        # saved at checkpoint
        self.level_groups_checkpoint = Level()
        self.coin_counter_checkpoint = 0

        # timer
        self.frame_count = None
        self.timer_string = None

        # map
        self.map = None
        self.player_start = None
        self.player_spawn = None
        self.total_world_shift = 0
        self.shift_factor = 0

    def load_data(self):
        """ load level times """
        with open(path.join(self.dir, HIGH_SCORES), 'w') as f:
            try:
                self.high_score = int(f.read())
            except IOError:
                self.high_score = 0

    def init_map(self, map_tiles):
        """ Initialized all sprites from the level """
        for t in map_tiles:
            # enemy
            if t.tile_id == 69:
                e = GroundCrawler(self, t.x, t.y, t.tile_id, self.map.ENEMY_SPEED)
                self.level_groups.death_tiles.add(e)
                self.level_groups.enemies.add(e)
                self.level_groups.all_sprites.add(e)
            # player
            elif t.tile_id == 80:
                self.player_spawn = (t.x, t.y)
            # jump pad
            elif t.tile_id == 74:
                p = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.platforms.add(p)
                self.level_groups.all_sprites.add(p)
                self.level_groups.jump_pads.add(p)
            # finish
            elif t.tile_id == 112:
                f = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.finishes.add(f)
                self.level_groups.all_sprites.add(f)
            # checkpoint
            elif t.tile_id == 67:
                c = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.checkpoints.add(c)
                self.level_groups.all_sprites.add(c)
            # Moving platform
            elif t.tile_id == 77:
                print("tiledata:" + str(t.data))
                c = MovingPlatform(self, t.x, t.y, t.tile_id, t.data)
                self.level_groups.platforms.add(c)
                self.level_groups.all_sprites.add(c)
            # AI border
            elif t.tile_id == 124:
                a = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.ai_borders.add(a)
                self.level_groups.all_sprites.add(a)
            # death tile
            elif t.tile_id in colorMap.death_tiles:
                d = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.death_tiles.add(d)
                self.level_groups.all_sprites.add(d)
            # coin
            elif t.tile_id == 99:
                c = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.coins.add(c)
                self.level_groups.all_sprites.add(c)
            # invisible tile
            elif t.tile_id == 33:
                i = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.all_sprites.add(i)
            # floor filler tile without collision
            elif t.tile_id == 120:
                f = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.all_sprites.add(f)
            # the rest is assumed to be a platforms
            else:
                p = Platform(t.x, t.y, t.tile_id, 1)
                self.level_groups.platforms.add(p)
                self.level_groups.all_sprites.add(p)

    def new(self, level):
        """ start new game, player lives set """
        self.level_groups = self.level_groups_checkpoint
        if self.map is None:
            self.map = Map(level)
            self.init_map(self.map.getTiles())

        player_properties = [self.map.PLAYER_ACC,
                             self.map.PLAYER_FRICTION,
                             self.map.PLAYER_GRAV,
                             self.map.PLAYER_JUMP]

        # if player has not reached a checkpoint, place on starting position
        if self.player_start is None:
            if self.player_spawn is None:
                self.player_spawn = (WIDTH / 2, HEIGHT / 2)
            self.player_start = self.player_spawn

        if self.player is None:
            self.player = Player(self, player_properties,
                                 TILESIZE, TILESIZE * 3 / 2)
            self.level_groups.all_sprites.add(self.player)
        else:
            self.player.vel.y = 0
            self.player.vel.x = 0
        self.player.set_start(self.player_start)

        thread = Thread(target=self.run())
        thread.start()
        thread.join()

    # Game loop methods
    def run(self):
        """ game loop """
        self.frame_count = 0
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            # todo put loop in thread and synchronize
            # Thread(target=self.update_sprites_on_screen()).start()
            self.clock.tick(FPS)

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

    def update(self):
        """ update all the things! """
        # update timer
        self.update_timer_string()
        # game loop updates
        self.level_groups.all_sprites.update()

        # check all die conditions
        if (self.player.rect.top > HEIGHT or
                pg.sprite.spritecollide(self.player, self.level_groups.death_tiles, False)):
            # start level again if you have enough lives left, otherwise stop playing
                self.has_won = False
                self.playing = False

        # check coin collision
        hits = pg.sprite.spritecollide(self.player, self.level_groups.coins, True)
        if hits:
            self.coin_counter += 1

        # check win conditions
        if pg.sprite.spritecollide(self.player, self.level_groups.finishes, False):
            self.has_won = True
            self.playing = False

        # check checkpoint collision
        hits = pg.sprite.spritecollide(self.player, self.level_groups.finishes, False)
        if hits:
            self.player_start = (hits[0].rect.x, hits[0].rect.y)
            self.level_groups_checkpoint = self.level_groups
            self.coin_counter_checkpoint = self.coin_counter

    def draw(self):
        """ game loop - drawing """
        self.screen.blit(self.bg, (0, 0))

        # self.sprites_on_screen.draw(self.screen)
        self.level_groups.all_sprites.draw(self.screen)

        self.draw_text("Lives: " + str(self.lives), 24, colorMap.BLACK, WIDTH / 2, 15)
        self.draw_text(self.timer_string, 24, colorMap.BLACK, WIDTH / 2, HEIGHT - 35)
        self.draw_text("Coins: " + str(self.coin_counter), 24, colorMap.BLACK, 50, 15)
        # after drawing everything, update the screen
        pg.display.flip()

    def quit(self):
        """ stops the game """
        if self.playing:
            self.playing = False
        self.running = False

    # Other methods
    def show_start_screen(self):
        """ game start screen """
        self.screen.fill(colorMap.WHITE)
        self.draw_text(TITLE, 48, colorMap.BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, colorMap.BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        # todo: display record times for each level...
        self.draw_text("Record time: " + str(self.high_score), 22, colorMap.BLACK, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        return self.wait_for_key()

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
        key = None
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    key_down = True
                    key = event.key
                if key_down and event.type == pg.KEYUP:
                    waiting = False
        return key

    def shift_world(self, shift_x):
        """ shift everything opposite of the change in x of the player """
        if self.player.rect.right > WIDTH * 2 / 3 and shift_x > 0:
            for sprite in self.level_groups.all_sprites:
                sprite.rect.right -= shift_x
            self.total_world_shift -= shift_x
        elif self.player.rect.left < WIDTH / 3 and shift_x < 0:
            for sprite in self.level_groups.all_sprites:
                sprite.rect.left -= shift_x
            self.total_world_shift -= shift_x

    # todo fix algorithm. Also, use more efficient buffering: only redraw moved elements
    # easy fix: use collision: make a rectangle that covers the entire display (not the map), and update on collision
    # execute every iteration, not only when moved
    def update_sprites_on_screen(self):
        shift_factor = abs(self.total_world_shift // TILESIZE)
        if (shift_factor - self.shift_factor) >= 1:
            self.shift_factor = shift_factor
            self.sprites_on_screen = pg.sprite.Group()
            for sprite in self.all_sprites:
                if sprite.rect.left < (WIDTH - 200) and sprite.rect.right > (0 + 200):
                    print("ON SCREEN, " + str(shift_factor))
                    self.sprites_on_screen.add(sprite)

    def reset_level(self):
        """ resets constants to start a fresh game """
        self.player_start = None
        self.player_spawn = None
        self.total_world_shift = 0
        self.level_groups_checkpoint = Level()
        self.level_groups = None
        self.player = None
        self.map = None

    def play_level(self, level, lives):
        """ play one level with the amount of lives given
            return True if level completed, else return False"""
        self.lives = lives
        while self.lives >= 1 and self.running:
            self.new(level)
            self.coin_counter = self.coin_counter_checkpoint
            if self.has_won:
                break
            self.lives -= 1

        # todo: add score to top of screen and go/win screen
        if self.has_won:
            print("YOU WON!")
            self.show_go_screen()
            return True
        else:
            print("YOU LOSE!")
            self.show_go_screen()
            return False


g = Game()
# m = Menu(g.screen)
while g.running:
    g.show_start_screen()
    level_index = 1
    print("level index: " + str(level_index))
    while level_index < len(PLAYLIST[0]) and g.play_level(PLAYLIST[0][level_index], g.lives):
        g.reset_level()
        level_index += 1
        print("level index: " + str(level_index))
    # todo: method for saving score and resetting score attributes
    g.reset_level()
    g.lives = PLAYER_LIVES
    g.coin_counter = 0
    g.score = 0
pg.quit()
