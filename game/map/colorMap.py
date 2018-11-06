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
SPIKE_DOWN  = None
SPIKE_UP    = None
SPIKE_LEFT  = None
LASER       = None
SPIKE_RIGHT = None
ANDROID     = None

# All byte-to-color mappings
#
#       PLEASE KEEP THIS MAP SORTED IN ASCENDING ORDER
#
colours = {
            10: RED,            # "\n"
            32: BLUE,           # " "
            33: I_TILE,         # "!"
            45: STDPLATFORM,    # "-"
            60: SPIKE_LEFT,     # "<"
            61: GRASS,          # "="
            62: SPIKE_RIGHT,    # ">"
            64: BLACK,          # "@"
            65: ANDROID,        # "A"
            66: MAPBORDER,      # "B"
            67: CHECKPOINT,     # "C"
            68: DEATHTILE,      # "D"
            69: ENEMY,          # "E"
            70: FLOORFILLER,    # "F"
            71: GREEN,          # "G"
            74: JUMPPAD,        # "J"
            76: LASER,          # "L"
            77: MOVINGPLATFORM, # "M"
            80: PLAYERSPAWN,    # "P"
            87: BROWN,          # "W"
            90: GRASSBLOCK,     # "Z"
            94: SPIKE_UP,       # "^"
            99: COIN,           # "c"
            100: I_DEATHTILE,   # "d"
            112: FINISH,        # "p"
            118: SPIKE_DOWN,    # "v"
            120: FLOORFILLER,   # "x"
            124: AIBORDER,      # "|"
        }
death_tiles = {68, 83, 100, 94, 118, 62, 60}
uses_image = {45, 61, 67, 68, 69, 70, 112, 99, 124, 33, 74, 90, 120, 94, 118, 62, 60, 76}
air_tiles = {32, 33, 77, 69}