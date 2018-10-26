# game options
TITLE = "Platformer"
WIDTH = 1280
HEIGHT = 720
TILESIZE = 20
FPS = 60
PLAYER_LIVES = 2
FONT_NAME = 'arial'
RECORDS_FILE = 'level_records.txt'

# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
# todo: use this player jump variable to jump
PLAYER_JUMP = 20

# starting platforms
# todo: replace with map reader!
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)