import pygame
from game.map.map import Map
import game.settings as settings

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

BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
RED   = (255, 0,   0  )

colours =   {
                71 : GREEN,
                32 : BLUE,
                87 : BROWN,
                10 : RED,
                64 : BLACK
            }

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    for t in mapTiles:
        pygame.draw.rect(mainSurface, colours[t.byte], (t.x, t.y, settings.TILESIZE, settings.TILESIZE))

    pygame.display.update()

    clock.tick(60)
