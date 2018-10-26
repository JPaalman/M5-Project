import os
from game.tiles.tile import Tile
from game import settings

class Map:
    """
        This class retrieves contents of a map file, puts all values into the proper variables and
        make them available for retrieving.
    """
    def __init__(self, mname):
        self.mapHeight = None
        self.mapWidth = None
        self.mapLayout = None
        self.mapName = None
        self.tileData = None

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
                data = self.findTileData(colnr, rownr)
                res.append(Tile(self.getX(colnr), self.getY(rownr), self.mapLayout[rownr][colnr], data))
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
        index += (len(self.mapLayout) + 1)

        # Load tile data
        self.tileData = self.getTileData(lines[index:])

        print("Map initiated:")
        print("Map name: " + self.mapName)
        print("Width: " + str(self.mapWidth))
        print("Height: " + str(self.mapHeight))
        print("\nMapdata:")
        for x in self.mapLayout:
            print(x)

    def cleanLines(self, ls):
        tempList = []

        for x in ls:
            tempList.append(x[:-1])
        ls = tempList

        out = []
        i = self.nextLine(ls, -1)

        while i < len(ls):
            out.append(ls[i])
            i = self.nextLine(ls, i)

        return out


    def nextLine(self, ls, index):
        for x in range(index + 1, len(ls) - 1):
            # TODO implement filtering for empty lines (not working atm)
            # TODO map data is being ignored, fix.
            if (len(ls[x]) > 0) and (ls[x][0] != "#"):
                return x
        return len(ls)

    def getParamValue(self, input):
        return input.split("=")[1]

    def getMapLayout(self, data):
        # TODO fix bug that includes the mapend line into the result
        # TODO implement padding and truncation
        res = []
        count = 0
        for x in data:
            count += 1
            if str(x) == "!MAPEND":
                return res
            res.append(bytearray(x, "ascii"))
        return res

    def getTileData(self, lines):
        values = []
        for x in lines:
            tmp = x.split("=")
            print(tmp)
            xy = tmp[0].split(",")
            print(xy)
            xVal = int(xy[0])
            yVal = int(xy[1])
            data = int(tmp[1])
            values.append([yVal, xVal, data])
        return values

    def findTileData(self, col, row):
        xCoord = row
        yCoord = col
        temp = None
        count = 0
        i = -1
        for x in self.tileData:
            if (x[0] == xCoord) and (x[1] == yCoord):
                temp = x
                i = count
                break
            count += 1
        if (i != -1) and (i < len(self.tileData)):
            del self.tileData[i]
        if temp is None:
            return 0;
        return temp[2]

    def getX(self, x):
        return settings.TILESIZE * x

    def getY(self, y):
        return settings.TILESIZE * y