from os import path

from game.map.map import Map
from game.sprites import *
from game.menu import Menu


class Game:
    """ platformer game """

    def __init__(self):
        """ initialize game window """
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF, 16)  # (0, pg.FULLSCREEN)[FULLSCREEN]
        pg.display.set_caption(TITLE)
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.playing = True
        self.has_won = False
        self.lives = PLAYER_LIVES
        self.coin_counter = 0
        self.dead = True

        self.old_rects = []

        # background
        self.bg = rM.getImage("bg.jpg", False)

        # level records
        self.dir = path.dirname(__file__)
        self.load_data()
        self.high_score = None

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

        # timer
        self.frame_count = 0
        self.timer_string = None

        # map
        self.player = None
        self.map = None
        self.finish = None
        self.player_start = None
        self.player_spawn = None
        self.total_world_shift = 0
        self.checkpoint_shift = 0
        self.checkpoint_coin_counter = 0
        self.shift_factor = 999

        # menu
        self.menu = Menu(self.screen)

        # sounds
        self.sound_counter = 0
        self.coin_sound = rM.getSound("coin.wav")
        self.checkpoint_sound = rM.getSound("Checkpoint.wav")
        self.die_sound = rM.getSound("steve_hurt.wav")

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
                self.death_tiles.add(e)
                self.enemies.add(e)
                self.all_sprites.add(e)
            # player
            elif t.tile_id == 80:
                self.player_spawn = (t.x, t.y)
            # jump pad
            elif t.tile_id == 74:
                p = Platform(t.x, t.y, t.tile_id, 1)
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
                f = Platform(t.x, t.y, t.tile_id, 1)
                self.finish = f
                self.all_sprites.add(f)
            # checkpoint
            elif t.tile_id == 67:
                c = Platform(t.x, t.y, t.tile_id, 1)
                self.checkpoints.add(c)
                self.all_sprites.add(c)
            # Moving platform
            elif t.tile_id == 77:
                print("tiledata:" + str(t.data))
                c = MovingPlatform(self, t.x, t.y, t.tile_id, t.data)
                self.platforms.add(c)
                self.all_sprites.add(c)
            # AI border
            elif t.tile_id == 124:
                a = Platform(t.x, t.y, t.tile_id, 1)
                self.ai_borders.add(a)
                self.all_sprites.add(a)
            # death tile
            elif t.tile_id in colorMap.death_tiles:
                d = Platform(t.x, t.y, t.tile_id, 1)
                self.death_tiles.add(d)
                self.all_sprites.add(d)
            # coin
            elif t.tile_id == 99:
                c = Platform(t.x, t.y, t.tile_id, 1)
                self.coins.add(c)
                self.all_sprites.add(c)
            # invisible tile
            elif t.tile_id == 33:
                i = Platform(t.x, t.y, t.tile_id, 1)
                self.all_sprites.add(i)
            # floor filler tile without collision
            elif t.tile_id == 120:
                f = Platform(t.x, t.y, t.tile_id, 1)
                self.all_sprites.add(f)
            # the rest is assumed to be a platforms
            else:
                p = Platform(t.x, t.y, t.tile_id, 1)
                self.platforms.add(p)
                self.all_sprites.add(p)

    def new(self, level):
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

        self.run()

    def run(self):
        """ game loop """
        draw_counter = 0
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            if draw_counter == 0:
                self.draw()
                draw_counter = 2
            draw_counter -= 1
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
        if self.player.rect.colliderect(self.finish.rect):
            self.has_won = True
            self.playing = False
            self.checkpoint_coin_counter = self.coin_counter

        # check checkpoint collision
        hits = pg.sprite.spritecollide(self.player, self.checkpoints, False)
        if hits:
            self.player_start = (hits[0].rect.x, hits[0].rect.y)
            self.checkpoint_shift = self.total_world_shift
            self.checkpoint_coin_counter = self.coin_counter
            if self.sound_counter == 0:
                pg.mixer.Sound.play(self.checkpoint_sound)
                self.sound_counter = 100
        if self.sound_counter > 0:
            self.sound_counter -= 1

        UPS = 5  # updates per second; checking sprites on screen
        if self.frame_count % (FPS // UPS) == 0:
            self.set_sprites_on_screen()

    def draw(self):
        """ game loop - drawing """
        self.screen.blit(self.map.bgImage, (0, 0))
        # self.screen.fill(colorMap.WHITE)

        self.sprites_on_screen.draw(self.screen)
        # self.all_sprites.draw(self.screen)

        self.draw_text("Lives: " + str(self.lives), 24, colorMap.BLACK, WIDTH - 60, 20)
        self.draw_text("Coins: " + str(self.coin_counter), 24, colorMap.BLACK, 60, 20)
        self.draw_text(self.timer_string, 24, colorMap.BLACK, WIDTH / 2, HEIGHT - 40)
        self.draw_text(self.map.mapName, 24, colorMap.BLACK, WIDTH / 2, 20)
        # after drawing everything, update the screen
        pg.display.flip()

    def draw2(self):
        # copy the background rather than blitting it to the display buffer
        # buffer is dumped when the drawing completes
        buffer = self.bg.copy()
        self.sprites_on_screen.draw(buffer)

        rects = []

        # get all onscreen sprite rects
        for sprite in self.sprites_on_screen:
            rects.append(sprite.rect)

        # after drawing everything, update the screen
        pg.display.update(rects + self.old_rects)

        self.old_rects = rects

    def quit(self):
        """ stops the game """
        if self.playing:
            self.playing = False
        self.running = False

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

    def play_level(self, level, lives, playlist_name, is_last):
        """ plays a specific level until win or no lives left """
        self.lives = lives
        while self.lives >= 1 and self.running:
            self.new(level)
            if self.has_won:
                break
            self.lives -= 1

        # todo: add score to top of screen and go/win screen
        if self.running:
            if self.has_won:
                print("YOU WON!")
                if not self.menu.finish(is_last, playlist_name, self.frame_count // 60, self.checkpoint_coin_counter):
                    self.quit()
                return True
            else:
                print("YOU LOSE!")
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
                                playlist_name, level_index == level_amount)):
            self.reset_level()
            level_index += 1
        # todo: method for saving score and reset score in reset_level
        self.lives = PLAYER_LIVES
        self.coin_counter = 0
        self.frame_count = 0


g = Game()
while g.running:
    index = g.menu.selectPlaylist()
    g.play_playlist(index)
pg.quit()