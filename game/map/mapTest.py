import pygame
from game.map.map import Map
import game.settings as settings
import game.map.colorMap as colorMap

pygame.init()
clock = pygame.time.Clock()

caption = 'Platformer'

mainSurface = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),0 ,32)
pygame.display.set_caption(caption)

mapObj = Map("MapTemplate.txt")
mapTiles = mapObj.getTiles()
for t in mapTiles:
    print(str(t.x) + " " + str(t.y) + " " + str(t.byte))
MAPHEIGHT = mapObj.mapHeight
MAPWIDTH = mapObj.mapWidth

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    for t in mapTiles:
        pygame.draw.rect(mainSurface, colorMap.colours[t.byte], (t.x, t.y, settings.TILESIZE, settings.TILESIZE))
    pygame.display.update()

    clock.tick(60)
