import os

# game options
FULLSCREEN = False
TITLE = "Platformer"
WIDTH = 1280
HEIGHT = 720
TILESIZE = 20
FPS = 60
FONT_NAME = 'arial'
RECORDS_FILE = 'level_records.txt'
PLAYER_LIVES = 5

# level files
LEVEL_1 = 'palette.txt'

# starting platforms
# todo: replace with map reader!
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

dirname = os.path.dirname(__file__)
bgImage = os.path.join(dirname, "bg.jpg")