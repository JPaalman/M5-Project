import game.settings as settings

class Tile:

    TILESIZE = settings.TILESIZE

    '''
    instance variables:
    x (x-coordinate top left of tile)
    y (y-coordinate top left of tile)
    w (width)
    h (height
    texturePath (path to texture)
    '''

    def __init__(self, new_x, new_y, new_byte, new_data):
        self.x = new_x
        self.y = new_y
        self.byte = new_byte
        self.data = new_data
        if self.data != 0:
            self.byte = 64
        #self.texturePath = self.setTexture()

    def setTexture(self):
        return ""
        # TODO select texture based on byte
