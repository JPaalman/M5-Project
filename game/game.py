from os import path

from game.map.map import Map
from game.menu import Menu
from game.sprites import *
from game import settings
import time

PROFILING = False
DRAW_TEXT = True


def format_timer(seconds):
    """ formates an integer seconds to a string in minutes : seconds """
    minutes = seconds // 60
    timer_string = "Time: {:02d}:{:02d}".format(int(minutes), int(seconds) % 60)
    return timer_string


class Game:
    """ platformer game """

    # Initialization of Game, high scores, map tiles and a new level

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
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.playing = True
        self.has_won = False
        self.lives = PLAYER_LIVES
        self.coin_counter = 0
        self.dead = True
        self.frame_count = 0
        self.total_seconds = 0
        self.dir = path.dirname(__file__)

        # init sprite Groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.death_tiles = pg.sprite.Group()
        self.checkpoints = pg.sprite.Group()
        self.ai_borders = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.sprites_on_screen = pg.sprite.Group()
        self.jump_pads = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.sprites_on_screen = pg.sprite.Group()
        self.finishes = pg.sprite.Group()

        # map
        self.player = None
        self.map = None
        self.player_start = None
        self.player_spawn = None
        self.total_world_shift = 0
        self.checkpoint_shift = 0
        self.checkpoint_coin_counter = 0
        self.shift_factor = 999
        self.last_checkpoint_rect = None
        self.map_quick_load = False

        # menu
        self.menu = Menu(self.screen)

        # sounds
        self.sound_counter = 0
        self.coin_sound = rM.getSound("coin.wav")
        self.checkpoint_sound = rM.getSound("Checkpoint.wav")
        self.die_sound = rM.getSound("steve_hurt.wav")
        self.win_sound = rM.getSound("finish.wav")
        self.lose_sound = rM.getSound("game-over.wav")

        # overlayed text info
        self.overlay_seconds = 0
        self.overlay_coins = 0
        self.overlay_lives = 0
        self.overlay_map_name = None

        # rendered text info
        self.rendered_seconds = None
        self.rendered_coins = None
        self.rendered_lives = None
        self.rendered_map_name = None

    def init_map(self, map_tiles):
        """ Initialized all sprites from the level """
        style = int(self.map.MAP_STYLE)
        print("map style: " + str(style))
        for t in map_tiles:
            # ghost
            if t.tile_id == 69:
                e = Ghost(self, t.x, t.y, t.tile_id, self.map.ENEMY_SPEED, style)
                self.death_tiles.add(e)
                self.enemies.add(e)
                self.all_sprites.add(e)
            # android
            elif t.tile_id == 65:
                e = GroundCrawler(self, t.x, t.y, t.tile_id, self.map.ENEMY_SPEED, style)
                self.death_tiles.add(e)
                self.enemies.add(e)
                self.all_sprites.add(e)
            # player
            elif t.tile_id == 80:
                self.player_spawn = (t.x, t.y)
            # jump pad
            elif t.tile_id == 74:
                p = Platform(t.x, t.y, t.tile_id, 1, style)
                self.platforms.add(p)
                self.all_sprites.add(p)
                self.jump_pads.add(p)
            # laser
            elif t.tile_id == 76:
                l = Laser(self, t.x, t.y, t.tile_id)
                self.platforms.add(l)
                self.all_sprites.add(l)
            # finish
            elif t.tile_id == 112:
                f = Platform(t.x, t.y, t.tile_id, 1, style)
                self.finishes.add(f)
                self.all_sprites.add(f)
            # checkpoint
            elif t.tile_id == 67:
                c = Platform(t.x, t.y, t.tile_id, 1, style)
                self.checkpoints.add(c)
                self.all_sprites.add(c)
            # Moving platform
            elif t.tile_id == 77:
                print("tiledata:" + str(t.data))
                c = MovingPlatform(self, t.x, t.y, t.tile_id, t.data, style)
                self.platforms.add(c)
                self.all_sprites.add(c)
            # AI border
            elif t.tile_id == 124:
                a = Platform(t.x, t.y, t.tile_id, 1, style)
                self.ai_borders.add(a)
                self.all_sprites.add(a)
            # death tile
            elif t.tile_id in colorMap.death_tiles:
                d = Platform(t.x, t.y, t.tile_id, 1, style)
                self.death_tiles.add(d)
                self.all_sprites.add(d)
            # coin
            elif t.tile_id == 99:
                c = Coin(t.x, t.y)
                self.coins.add(c)
                self.all_sprites.add(c)
            # invisible tile
            elif t.tile_id == 33:
                i = Platform(t.x, t.y, t.tile_id, 1, style)
                self.all_sprites.add(i)
            # floor filler tile without collision
            elif t.tile_id == 120:
                f = Platform(t.x, t.y, t.tile_id, 1, style)
                self.all_sprites.add(f)
            elif t.tile_id == 83:
                s = Platform(t.x, t.y, t.tile_id, 1, style)
                self.all_sprites.add(s)
            # the rest is assumed to be a platforms
            else:
                # print("WARNING: Creating platform for unknown tile_id: " + str(t.tile_id))
                p = Platform(t.x, t.y, t.tile_id, 1, style)
                self.platforms.add(p)
                self.all_sprites.add(p)

    def new(self, level, play_music):
        """ start new game, player lives set """
        if self.map is None:
            self.all_sprites.empty()
            self.platforms.empty()
            self.death_tiles.empty()
            self.checkpoints.empty()
            self.ai_borders.empty()
            self.coins.empty()
            self.sprites_on_screen.empty()
            self.jump_pads.empty()
            self.enemies.empty()
            self.finishes.empty()
            self.map = Map(level)
            self.init_map(self.map.getTiles())
            if self.map.FFT_HIGH is None:
                self.map.FFT_HIGH = settings.DEFAULT_FFT_HIGH
            if self.map.FFT_LOW is None:
                self.map.FFT_LOW = settings.DEFAULT_FFT_LOW

            if play_music:
                rM.loadMusic(self.map.BACKGROUND_MUSIC)
                pg.mixer.music.play(-1)

        player_properties = [self.map.PLAYER_ACC,
                             self.map.PLAYER_FRICTION,
                             self.map.PLAYER_GRAV,
                             self.map.PLAYER_JUMP]

        # if player has not reached a checkpoint, place on starting position
        if self.player_start is None:
            if self.player_spawn is None:
                self.player_spawn = (WIDTH / 2, HEIGHT / 2)
            self.player_start = self.player_spawn

        for sprite in self.all_sprites:
            sprite.rect.right += (self.checkpoint_shift - self.total_world_shift)
        self.total_world_shift = self.checkpoint_shift

        if self.player is None:
            self.player = Player(self, player_properties,
                                 TILESIZE, TILESIZE * 3 / 2)
            self.all_sprites.add(self.player)
        else:
            self.player.vel.y = 0
            self.player.vel.x = 0
        self.player.set_start(self.player_start)

        self.map_quick_load = True
        self.run()

    # Game loop; run to call events, update and draw

    def run(self):
        """ game loop """
        self.playing = True
        while self.playing:
            old_time = time.time() * 1000
            self.events()
            if PROFILING:
                print("handling events took " + str(int(time.time() * 1000 - old_time)) + " milliseconds")
                old_time = time.time() * 1000
            self.update()
            if PROFILING:
                print("updating took " + str(int(time.time() * 1000 - old_time)) + " milliseconds")
                old_time = time.time() * 1000
            if self.frame_count % 2 == 0:
                self.draw()
            if PROFILING:
                print("drawing took " + str(int(time.time() * 1000 - old_time)) + " milliseconds\n")
            self.clock.tick(FPS)
        if self.dead:
            self.update()
            self.draw()
            pg.mixer.Sound.play(self.die_sound)
            time.sleep(1)
            self.dead = False

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

        """
        # Handle FPGA jump input
        if self.map.FFT_LOW <= self.spiController.fft <= self.map.FFT_HIGH and self.spiController.rms >= settings.RMS_JUMP_THRESHOLD:
            self.player.jump(self.spiController.rms / settings.RMS_JUMP_DIVSOR)
        """

    def update(self):
        """ update all the things! """
        # game loop updates
        self.all_sprites.update()

        # check all die conditions
        if (self.player.rect.top > HEIGHT or
                pg.sprite.spritecollide(self.player, self.death_tiles, False)):
            # start level again if you have enough lives left, otherwise stop playing
            self.has_won = False
            self.playing = False
            self.coin_counter = self.checkpoint_coin_counter
            self.shift_factor = 999
            self.dead = True

        # check coin collision
        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        if hits:
            pg.mixer.Sound.play(self.coin_sound)
            self.coin_counter += 1

        # check win conditions
        hits = pg.sprite.spritecollide(self.player, self.finishes, True)
        if hits:
            self.has_won = True
            self.playing = False
            self.checkpoint_coin_counter = self.coin_counter
            self.dead = False

        # check checkpoint collision
        hits = pg.sprite.spritecollide(self.player, self.checkpoints, False)
        if hits:
            checkpoint_pos = (hits[0].rect.x, hits[0].rect.y)
            # if this was not last visited checkpoint, only then play sound
            if self.last_checkpoint_rect != hits[0].rect:
                pg.mixer.Sound.play(self.checkpoint_sound)
                self.last_checkpoint_rect = hits[0].rect

            self.player_start = checkpoint_pos
            self.checkpoint_shift = self.total_world_shift
            self.checkpoint_coin_counter = self.coin_counter

        UPS = 5  # updates per second; checking sprites on screen
        if self.map_quick_load or self.frame_count % (FPS // UPS) == 0:
            self.map_quick_load = False
            self.set_sprites_on_screen()

        if self.frame_count % FPS == 0:
            self.total_seconds = self.frame_count / FPS

        self.frame_count += 1

    def draw(self):
        """ game loop - drawing """
        old_time = time.time()

        self.screen.blit(self.map.bgImage, (0, 0))

        if PROFILING:
            print("    background took " + str(int((time.time() - old_time) * 1000)) + " milliseconds")
            old_time = time.time()

        self.sprites_on_screen.draw(self.screen)

        if PROFILING:
            print("    sprites took " + str(int((time.time() - old_time) * 1000)) + " milliseconds")
            old_time = time.time()

        # for the overlayed text, check if a new render has to be made, otherwise use the exisiting text surface
        if DRAW_TEXT:
            if self.rendered_lives is None or self.lives != self.overlay_lives:
                self.overlay_lives = self.lives
                self.rendered_lives = self.render_text("Lives: " + str(self.lives), 24, colorMap.BLACK)
            self.draw_text_surface(self.rendered_lives, WIDTH - 60, 20)

            if self.rendered_coins is None or self.coin_counter != self.overlay_coins:
                self.overlay_coins = self.coin_counter
                self.rendered_coins = self.render_text("Coins: " + str(self.coin_counter), 24, colorMap.BLACK)
            self.draw_text_surface(self.rendered_coins, 60, 20)

            if self.rendered_seconds is None or self.total_seconds != self.overlay_seconds:
                self.overlay_seconds = self.total_seconds
                self.rendered_seconds = self.render_text(format_timer(self.total_seconds), 24, colorMap.BLACK)
            self.draw_text_surface(self.rendered_seconds, WIDTH / 2, HEIGHT - 40)

            if self.rendered_map_name is None or self.map.mapName != self.overlay_map_name:
                self.overlay_map_name = self.map.mapName
                self.rendered_map_name = self.render_text(self.map.mapName, 24, colorMap.BLACK)
            self.draw_text_surface(self.rendered_map_name, WIDTH / 2, 20)
            if PROFILING:
                print("    text took " + str(int((time.time() - old_time) * 1000)) + " milliseconds")
                old_time = time.time()

        pg.display.flip()

        if PROFILING:
            print("    update took " + str(int((time.time() - old_time) * 1000)) + " milliseconds")

    def quit(self):
        """ stops the game """
        if self.playing:
            self.playing = False
        self.running = False

    # Methods regarding drawing to / updating the screen surface

    def draw_text_surface(self, text_surface, x, y):
        """ draw text to the screen at position x, y """
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def render_text(self, text, size, color):
        """ renders text to a surface """
        """ CPU INTENSIVE """
        if PROFILING:
            print("RENDERING: " + text)
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        return text_surface

    def shift_world(self, shift_x):
        """ shift everything opposite of the change in x of the player """
        if self.player.rect.right > WIDTH * 2 / 3 and shift_x > 0:
            for sprite in self.all_sprites:
                sprite.rect.right -= shift_x
            self.total_world_shift -= shift_x
        elif self.player.rect.left < WIDTH / 3 and shift_x < 0:
            for sprite in self.all_sprites:
                sprite.rect.left -= shift_x
            self.total_world_shift -= shift_x

    def set_sprites_on_screen(self):
        """ sets sprites_on_screen to only include sprites that are on screen """
        """ this update is only done after a world shift of 10 tiles """
        shift_factor = self.total_world_shift // (TILESIZE * 10)
        if shift_factor != self.shift_factor:
            self.shift_factor = shift_factor
            self.sprites_on_screen.empty()

            for sprite in self.all_sprites:
                if sprite.rect.left < (WIDTH + TILESIZE * 15) and sprite.rect.right > (0 - TILESIZE * 15):
                    self.sprites_on_screen.add(sprite)

    # Used to play (a series of) levels

    def reset_level(self):
        """ resets constants to start a fresh game """
        self.player_start = None
        self.player_spawn = None
        self.total_world_shift = 0
        self.checkpoint_shift = 0
        self.checkpoint_coin_counter = 0
        self.map = None
        self.player = None
        self.shift_factor = 999
        self.lives = PLAYER_LIVES
        self.last_checkpoint_rect = None

    def play_level(self, level, lives, playlist_name, is_last, play_music):
        """ plays a specific level until win or no lives left """
        self.lives = lives
        while self.lives >= 1 and self.running:
            self.new(level, play_music)
            if self.has_won:
                break
            self.lives -= 1

        # todo: add score to top of screen and go/win screen
        if self.running:
            if self.has_won:
                print("YOU WON!")
                if is_last:
                    pg.mixer.music.stop()
                    pg.mixer.Sound.play(self.win_sound)
                if not self.menu.finish(is_last, playlist_name, self.frame_count // 60, self.checkpoint_coin_counter):
                    self.quit()
                return True
            else:
                print("YOU LOSE!")
                pg.mixer.music.stop()
                pg.mixer.Sound.play(self.lose_sound)
                if not self.menu.gameOver():
                    self.quit()
                return False

    def play_playlist(self, playlist_index):
        """ plays a specific playlist until all levels completed or no lives left """
        level_index = 1
        level_amount = len(PLAYLIST[playlist_index]) - 1
        playlist_name = PLAYLIST[playlist_index][0]
        self.reset_level()
        while (level_index <= level_amount
               and g.play_level(PLAYLIST[playlist_index][level_index], g.lives,
                                playlist_name, level_index == level_amount, level_index == 1)):
            self.reset_level()
            level_index += 1
        # todo: method for saving score and reset score in reset_level
        self.lives = PLAYER_LIVES
        self.coin_counter = 0
        self.frame_count = 0


g = Game()
while g.running:
    index = g.menu.selectPlaylist()
    if index == -1:
        g.quit()
    else:
        g.play_playlist(index)
pg.quit()
