# coding=utf-8
# Definitions of all colors

# Standard colors
BLACK       = (0,   0,   0  )
BROWN       = (153, 76,  0  )
GREEN       = (0,   255, 0  )
BLUE        = (0,   0,   255)
RED         = (255, 0,   0  )
WHITE       = (255, 255, 255)
MOVINGPLATFORM = (25, 23, 54)

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
SPIKE       = None
JUMPPAD     = None
GRASSBLOCK  = None

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
            74: JUMPPAD,        # "J"
            77: MOVINGPLATFORM, # "M"
            80: PLAYERSPAWN,    # "P"
            83: SPIKE,          # "S"
            87: BROWN,          # "W"
            90: GRASSBLOCK,     # "Z"
            99: COIN,           # "c"
            100: I_DEATHTILE,   # "d"
            112: FINISH,        # "p"
            124: AIBORDER,      # "|"
            120: FLOORFILLER    # "•"
        }
death_tiles = {68, 83, 100}
uses_image = {45, 61, 67, 68, 69, 70, 112, 99, 124, 33, 74, 83, 90, 120}
airtiles = {32, 77, 69}