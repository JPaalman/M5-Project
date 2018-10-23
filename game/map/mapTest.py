import pygame
import game.map as mp

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
caption = 'Platformer'

mainSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0 ,32)
pygame.display.set_caption(caption)

mapObj = mp.Map("MapTemplate")
tilemap = mapObj.getMap()

MAPHEIGHT = 6
MAPWIDTH = 8
TILESIZE = 100

BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
RED   = (255, 0,   0  )

colours =   {
                71 : GREEN,
                32 : BLUE,
                87  : BROWN,
            }

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mainSurface

    #loop through ech row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(mainSurface, colours[tilemap[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    pygame.display.update()

    clock.tick(60)
main()
