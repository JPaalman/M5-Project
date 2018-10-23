import os
from game.tiles.tile import Tile
from game import settings

tileSize = 20

class Map:

    def __init__(self, mname):
        self.mapHeight = None
        self.mapWidth = None
        self.mapLayout = None
        self.mapName = None

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, mname)
        file_object = open(filename, 'r')
        self.rawMapLines = file_object.readlines()
        self.initMap(self.rawMapLines)

    def getTiles(self):
        res = []
        rownr = 0
        print(len(self.mapLayout))
        print(len(self.mapLayout[0]))
        while rownr < len(self.mapLayout):
            colnr = 0
            while colnr < len(self.mapLayout[rownr]):
                # TODO implement inserting tile data in constructor
                res.append(Tile(self.getX(colnr), self.getY(rownr), self.mapLayout[rownr][colnr], 0))
                colnr += 1
            rownr += 1
        return res

    def initMap(self, lines):

        lines = self.cleanLines(lines)

        index = 0;

        # Read map name
        self.mapName = self.getParamValue(lines[index])
        index += 1

        # Read map height
        self.mapHeight = int(float(self.getParamValue(lines[index])))
        index += 1

        # Read map width
        self.mapWidth = int(float(self.getParamValue(lines[index])))
        index += 1

        # Load maplayout
        self.mapLayout = self.getMapLayout(lines[index:])

        # Load tile data
        # TODO implement

        print("Map initiated:")
        print("Map name: " + self.mapName)
        print("Width: " + str(self.mapWidth))
        print("Height: " + str(self.mapHeight))
        print("\nMapdata:")
        for x in self.mapLayout:
            print(x)

    def cleanLines(self, list):

        tempList = []
        for x in list:
            tempList.append(x[:-1])
        list = tempList

        out = []
        i = self.nextLine(list, -1)

        while i < len(list):
            out.append(list[i])
            i = self.nextLine(list, i)

        return out


    def nextLine(self, list, index):
        for x in range(index + 1, len(list) - 1):
            # TODO implement filtering for empty lines (not working atm)
            # TODO map data is being ignored, fix.
            if (len(list[x]) > 0) and (list[x][0] != "#"):
                return x
        return len(list)

    def getParamValue(self, input):
        return input.split("=")[1]

    def getMapLayout(self, data):
        # TODO fix bug that includes the mapend line into the result
        # TODO implement padding and truncation
        res = []
        for x in data:
            if str(x) == "!MAPEND":
                return res
            res.append(bytearray(x, "ascii"))
        return res

    def getX(self, x):
        return tileSize * x

    def getY(self, y):
        return tileSize * y