import pygame
import color as c

pygame.init()
clock = pygame.time.Clock()

window_width = 800
window_height = 600
caption = 'Platformer'

gameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(caption)

pygame.display.update()

gameExit = False

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0

step_size = 4
jump_factor = 8

while not gameExit:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            gameExit = True;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -step_size
            elif event.key == pygame.K_RIGHT:
                lead_x_change = step_size
            elif event.key == pygame.K_UP:
                lead_y_change = -jump_factor

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and lead_x_change < 0:
                lead_x_change = 0
            elif event.key == pygame.K_RIGHT and lead_x_change > 0:
                lead_x_change = 0

    lead_x += lead_x_change
    lead_y += lead_y_change

    gameDisplay.fill(c.white)
    pygame.draw.rect(gameDisplay, c.black, [lead_x, lead_y, 50, 50])
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()