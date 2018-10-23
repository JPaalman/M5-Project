import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.running = True

    def new(self):
        # start new game
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
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop updates
        self.all_sprites.update()
        if self.player.vel.y > 0:
            # check for collision between player and platforms
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
        # if player reaches sides of screen, move the rest the opposite way
        if self.player.rect.left <= WIDTH / 4 or self.player.rect.right >= WIDTH * 3 / 4:
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x


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
        #after drawing everything, update the screen
        pg.display.flip()

    def show_start_screen(self):
        # game start screen
        pass

    def show_go_screen(self):
        # game over / continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
