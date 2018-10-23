import pygame as pg


class Player(pg.sprite.Sprite):
    ACCELERATION = 60 / FPS  # dummy value
    FRICTION = 0.5  # dummy value
    GRAVITY = 1  # dummy value
    LIFE = 5

    def __init__(self, x, y, h, w):
        super.__init__()

        self.x = x  # x position
        self.y = y  # y position
        self.h = h  # height
        self.w = w  # width

        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, GRAVITY)

        self.rect = pg.Rect(x, y, w, h)

        self.image = pg.Surface(w, h)
        self.image.fill(RED)
        # self.image = pg.image.load()

    def update(self):
        # key updates
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x -= self.a
        if keys[pygame.K_RIGHT]:
            self.acc.x += self.a
        # test jumping function
        if keys[pygame.K_SPACE]:
            self.vel.y = -20

        # friction
        self.acc.x += self.vel.x * FRICTION

        # update vel and pos
        self.vel.x += self.acc.x
        self.x += self.vel.x

        self.vel.y += self.acc.y
        self.y += self.vel.y

        # handle collision
        self.handleCollision()

    def handleCollision(self):
        if self.rect.colliderect(enemy.rect):
            while self.rect.colliderect(tile.rect):
                self.pos.y += 1;
            self.acc.y = 0;
            self.vel.x = 0;
