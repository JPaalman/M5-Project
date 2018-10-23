class Tile:

    TILESIZE = 20

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
        #self.texturePath = self.setTexture()

    def setTexture(self):
        return ""
        # TODO select texture based on byte
