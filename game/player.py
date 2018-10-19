import pygame
import color as c

class Player(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((75, 50))
        self.image.fill(c.red)
        self.rect = self.image.get_rect()
        self.speed = 5

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom < self.screen.get_height():
            self.rect.bottom += self.speed

    def moveRight(self):
        if self.rect.right < self.screen.get_width():
            self.rect.right += self.speed

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.right -= self.speed

    def collide(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            return True
        else:
            return False