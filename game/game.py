import pygame as pg
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load level times
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, RECORDS_FILE), 'w') as f:
            try:
                self.records = int(f.read())
            except:
                self.records = 0

    def new(self, lives):
        # start new game, player lives set
        self.lives = lives
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # game loop
        self.frame_count = 0
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
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
            self.player.pos.x -= max(self.player.vel.x, 2)
            for plat in self.platforms:
                plat.rect.right -= max(self.player.vel.x, 2)
        elif  self.player.rect.left < WIDTH / 3:
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.right -= self.player.vel.x

        # check all die conditions
        if self.player.rect.top > HEIGHT:
            if (self.lives > 1):
                self.new(self.lives - 1)
            else:
                self.playing = False
        #todo: killed by enemy

    def events(self):
        # game loop event
        for event in pg.event.get():
            # check for close window event
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # game loop draw
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text("Lives: " + str(self.lives), 24, BLACK, WIDTH / 2, 15)
        self.draw_text(self.timer_string, 24, BLACK, WIDTH / 2, HEIGHT - 30)
        #after drawing everything, update the screen
        pg.display.flip()

    def show_start_screen(self):
        # game start screen
        self.screen.fill(WHITE)
        self.draw_text(TITLE, 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        # todo: display record times for each level...
        self.draw_text("Record time: " + str(self.records), 22, BLACK, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # if game is closed mid game, skip the game over screen
        if not self.running:
            return

        # game over / continue
        self.screen.fill(WHITE)
        self.draw_text("GAME OVER", 48, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to start", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)

        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update_timer_string(self):
        if self.frame_count % FPS == 0:
            print("updating")
            self.total_seconds = self.frame_count // FPS
            minutes = self.total_seconds // 60
            seconds = self.total_seconds % 60
            self.timer_string = "Time: {:02d}:{:02d}".format(minutes, seconds)
        self.frame_count += 1

    def wait_for_key(self):
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
    g.new(PLAYER_LIVES)
    g.show_go_screen()

pg.quit()
