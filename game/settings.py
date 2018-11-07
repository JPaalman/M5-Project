import os

# game options
FULLSCREEN = False
TITLE = "Platformer"
WIDTH = 1280
HEIGHT = 720
TILESIZE = 20
FPS = 48
FONT_NAME = 'arial'
HIGH_SCORES = 'high_scores.json'
PLAYER_LIVES = 5
DEFAULT_MOVING_PLATFORM_SIZE = 6
LASER_UPTIME = 1
LASER_DOWNITME = 2
POINTS_PER_COIN = 1500
POINTS_LOSS_PER_SECOND = 100
BASE_POINTS = 20000
RMS_JUMP_THRESHOLD = 20
RMS_JUMP_DIVSOR = 45

# level files
PLAYLIST = [["oebele playlist", "Oebele_map.txt", "palette.txt"],
            ["nils playlist", "junglemadness.txt", "jungle2.txt"],
            ["Annefleur playlist", "annefleur_map.txt"]]

dirname = os.path.dirname(__file__)
bgImage = os.path.join(dirname, "bg.jpg")
main_menu_image = "main_menu.png"
highscores_file = "high_scores.json"
game_over_image = "game_over.png"
finish_image = "finish.png"

# texture styles
NORMAL = 0
JUNGLE = 1
