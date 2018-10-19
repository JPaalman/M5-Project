import pygame
from pygame.locals import *
import color as c
import player

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
caption = 'Platformer'

mainSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0 ,32)
pygame.display.set_caption(caption)

myPlayer = player.Player(mainSurface)
myPlayer.rect.centerx = mainSurface.get_width() / 2
myPlayer.rect.centery = mainSurface.get_height() / 2

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    mainSurface.fill(c.white)

    if pygame.key.get_pressed()[K_UP]:
        myPlayer.moveUp()
    if pygame.key.get_pressed()[K_DOWN]:
        myPlayer.moveDown()
    if pygame.key.get_pressed()[K_RIGHT]:
        myPlayer.moveRight()
    if pygame.key.get_pressed()[K_LEFT]:
        myPlayer.moveLeft()

    mainSurface.blit(myPlayer.image, myPlayer.rect)
    pygame.display.update()

    clock.tick(60)

main()
