import pygame
import tile


class Player(pygame.sprite.Sprite):
    HEIGHT = 30
    WEIGHT = 10
    WIDTH = 20

    def __init__(self):
        # init superclass Sprite
        pygame.sprite.Sprite.__init__(self)

        # define physic vars
        # todo find appropriate starting values
        self.acc = vec(0, 0)
        self.life = 5;
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.weight = WEIGHT

        # load player image
        # todo actually load an image instead of a hitbox
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill("#000000")
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        # update gravity
        # todo update to use weight
        self.acc.y += 1
        # todo implement friction

        # key listener
        # todo implement more defined physics
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x -= 1
        if keys[pygame.K_RIGHT]:
            self.acc.x += 1
        # test jumping function
        if keys[pygame.K_SPACE]:
            self.vel.y = -20

        # handle collision
        self.handleCollision()

    def handleCollision(self):
        if self.rect.colliderect(tile.rect):
            while self.rect.colliderect(tile.rect):
                self.pos.y += 1;
            self.acc.y = 0;
            self.vel.x = 0;
