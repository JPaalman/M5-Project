import os

from game import settings
import game.tiles


class Map:

    PADDING_CHAR = 32
    MAPBORDER_CHAR = 66

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

        file_object = open(filename, )
        self.rawMapLines = file_object.readlines()
        self.initMap(self.rawMapLines)

    def getTiles(self):
        """
        Converts all data stored in the map file to Tile objects
        :return: Tile[] of tiles representing the map
        """
        res = []
        rownr = 0
        print(len(self.mapLayout))
        while rownr < len(self.mapLayout):
            colnr = 0
            while colnr < len(self.mapLayout[rownr]):
                if self.mapLayout[rownr][colnr] != 32:
                    data = self.findTileData(colnr, rownr)
                    res.append(game.tiles.Tile(self.getX(colnr), self.getY(rownr), self.mapLayout[rownr][colnr], data))
                colnr += 1
            rownr += 1
        return res

    def initMap(self, lines):
        """
        Initializes all the instance variables by reading the file contents and
        converting the contents to their proper representation
        :param lines: Array of raw lines retrieved from the map file
        """
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

        index += len(self.mapLayout) + 1

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
        """
        Cleans the input lines by removing newline characters and ignoring empty lines or comment
        lines that start with '#'
        :param ls: The list that you want to clean
        :return: The cleaned list
        """
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
        """
        Returns the index of the next line that contains information.
        Emtpy lines or comment lines starting with '#' are skipped.
        :param ls: List with possibly relevant values.
        :param index: The last index read by the program
        :return: The index of the next line that is relevant
        """
        for x in range(index + 1, len(ls) - 1):
            if (len(ls[x]) > 0) and (ls[x][0] != "#") and (ls[x][0] != 10):
                return x
        return len(ls)

    def getParamValue(self, input):
        """
        Retrieves the string value of a parameter stored in the map file
        :param input: [PARAMNAME]=[VALUE]
        :return: VALUE
        """
        return input.split("=")[1]

    def getMapLayout(self, data):
        """
        Processes the raw lines that represent the map to a complete map. This includes
        adding padding to lines if they are shorter than the MAPWIDTH param in the map file specifies,
        and truncates lines if they are longer than the MAPWIDTH specifies. The same padding and truncation is applied
        to the map vertically. The map is padded with "space" characters, and border characters at the borders.
        :param data: The raw lines that represent the map layout itself.
        :return: A matrix of bytes that contains the byte for every tile on the map.
        """
        res = []
        padding = [self.PADDING_CHAR] * self.mapWidth
        padding[0] = self.MAPBORDER_CHAR
        padding[len(padding) - 1] = self.MAPBORDER_CHAR

        bottom_padding = [self.MAPBORDER_CHAR] * self.mapWidth

        i = 0
        while (i < len(data)) and (data[i] != "!MAPEND") and len(res) != self.mapHeight + 1:
            if len(res) == self.mapHeight:
                return res

            add = bytearray(data[i][:self.mapWidth], "ascii")
            if len(add) < self.mapWidth:
                while len(add) < self.mapWidth - 1:
                    if i == 0:
                        add.append(self.MAPBORDER_CHAR)
                    else:
                        add.append(self.PADDING_CHAR)
                add.append(self.MAPBORDER_CHAR)
            res.append(add)
            i += 1

        if len(res) != self.mapHeight:
            while len(res) < self.mapHeight - 1:
                res.append(padding)
            res.append(bottom_padding)

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