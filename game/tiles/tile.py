class Tile:

    self.TILESIZE = 20

    '''
    instance variables:
    x (x-coordinate top left of tile)
    y (y-coordinate top left of tile)
    w (width)
    h (height
    texturePath (path to texture)
    '''

    def __init__(self, x, y, byte, data):
        self.x = x
        self.y = y
        self.byte = byte
        self.data = data
        self.setTexture()

    def setTexture(self):
        self.byte
        self.texturePath
        # TODO select texture based on byte
