import pygame
from game.map.map import Map

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
caption = 'Platformer'

mainSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0 ,32)
pygame.display.set_caption(caption)

mapObj = Map("MapTemplate")
mapTiles = mapObj.getTiles()
for t in mapTiles:
    print(str(t.x) + " " + str(t.y) + " " + str(t.byte))
MAPHEIGHT = mapObj.mapHeight
MAPWIDTH = mapObj.mapWidth
TILESIZE = 100

BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
RED   = (255, 0,   0  )

colours =   {
                71 : GREEN,
                32 : BLUE,
                87 : BROWN,
                10 : RED
            }

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mainSurface

    for t in mapTiles:
        pygame.draw.rect(mainSurface, colours[t.byte], (t.x, t.y, 20, 20))

    pygame.display.update()

    clock.tick(60)
main()
