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
STDPLATFORM = (53,  72,  104)
GRASS       = (48,  150, 51 )
DEATHTILE   = (237, 109, 30 )
FLOORFILLER = (124, 76,  28 )
FINISH      = (255, 215, 0  )

# Invisible tiles
MAPBORDER   = None
PLAYERSPAWN = None
I_DEATHTILE = None
AIBORDER    = None

# All byte-to-color mappings
#
#       PLEASE KEEP THIS MAP SORTED IN ASCENDING ORDER
#
colours = {
            10: RED,            # "\n"
            32: BLUE,           # " "
            45: STDPLATFORM,    # "-"
            61: GRASS,          # "="
            64: BLACK,          # "@"
            66: MAPBORDER,      # "B"
            68: DEATHTILE,      # "D"
            70: FLOORFILLER,    # "F"
            71: GREEN,          # "G"
            80: PLAYERSPAWN,    # "P"
            87: BROWN,          # "W"
            100: I_DEATHTILE,   # "d"
            112: FINISH,        # "p"
            124: AIBORDER       # "|"
        }