import os

class Map:

    def __init__(self, mname):
        self.mapName = mname

    def getMap(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, self.mapName)
        file_object  = open(filename, 'r')
        lines = file_object.readlines()

        mapArray = []
        for x in lines:
            mapArray.append(bytes(x.rstrip(), "ascii"))
            print(mapArray)
        print(mapArray[5][7])
        return mapArray