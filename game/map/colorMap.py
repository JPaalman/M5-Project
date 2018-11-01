# coding=utf-8
# Definitions of all colors

# Standard colors
BLACK       = (0,   0,   0  )
BROWN       = (153, 76,  0  )
GREEN       = (0,   255, 0  )
BLUE        = (0,   0,   255)
RED         = (255, 0,   0  )
WHITE       = (255, 255, 255)

# Game colors
STDPLATFORM = None  # (0,   60,  99 )
GRASS       = None  # (48,  150, 51 )
DEATHTILE   = None  # (237, 109, 30 )
FLOORFILLER = None  # (124, 76,  28 )
FINISH      = None  # (255, 215, 0  )

# Invisible tiles
MAPBORDER   = None
PLAYERSPAWN = None
I_DEATHTILE = None
AIBORDER    = None
CHECKPOINT  = None
I_TILE      = None
ENEMY       = None
COIN        = None

# All byte-to-color mappings
#
#       PLEASE KEEP THIS MAP SORTED IN ASCENDING ORDER
#
colours = {
            10: RED,            # "\n"
            32: BLUE,           # " "
            33: I_TILE,         # "!"
            45: STDPLATFORM,    # "-"
            61: GRASS,          # "="
            64: BLACK,          # "@"
            66: MAPBORDER,      # "B"
            67: CHECKPOINT,     # "C"
            68: DEATHTILE,      # "D"
            69: ENEMY,          # "E"
            70: FLOORFILLER,    # "F"
            71: GREEN,          # "G"
            80: PLAYERSPAWN,    # "P"
            87: BROWN,          # "W"
            100: I_DEATHTILE,   # "d"
            112: FINISH,        # "p"
            124: AIBORDER,      # "|"
            99: COIN            # "c"
        }
death_tiles = {68, 100}