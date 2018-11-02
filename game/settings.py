import os

# game options
FULLSCREEN = False
TITLE = "Platformer"
WIDTH = 1280
HEIGHT = 720
TILESIZE = 20
FPS = 60
FONT_NAME = 'arial'
HIGH_SCORES = 'high_scores.txt'
PLAYER_LIVES = 5

# level files
PLAYLIST = [
    ["test playlist", "Oebele_map.txt", "palette.txt"]
]




LEVEL_1 = 'Oebele_map.txt'
LEVELS = ["palette.txt",
          "Oebele_map.txt"]

dirname = os.path.dirname(__file__)
bgImage = os.path.join(dirname, "bg.jpg")
