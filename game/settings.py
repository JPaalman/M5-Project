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
DEFAULT_MOVING_PLATFORM_SIZE = 6

# level files
PLAYLIST = [["test playlist", "Oebele_map.txt", "palette.txt"],
            ["yeetlist", "map.txt", "othermap.txt"],
            ["list", "txt.txt", "woop.txt"]]

dirname = os.path.dirname(__file__)
bgImage = os.path.join(dirname, "bg.jpg")
main_menu_image = "main_menu.png"
highscores_file = "high_scores.txt"
game_over_image = "game_over.png"
