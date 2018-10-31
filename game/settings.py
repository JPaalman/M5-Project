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

dirname = os.path.dirname(__file__)
bgImage = os.path.join(dirname, "bg.jpg")