import os

from game import settings
import game.tiles
from game.map.colorMap import air_tiles
from game.resources import resourceManager
from game.resources.textures import textureManager as tM


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
        self.bgImage = None
        self.tileData = None
        self.PLAYER_ACC = None
        self.PLAYER_ACC = None
        self.PLAYER_FRICTION = None
        self.PLAYER_GRAV = None
        self.PLAYER_JUMP = None
        self.BACKGROUND_IMAGE = None
        self.ENEMY_SPEED = None
        self.PLATFORM_SPEED = None
        self.BACKGROUND_MUSIC = None
        self.rawMapLines = resourceManager.getMap(mname)
        self.initMap(self.rawMapLines)

    def getTiles(self):
        """
        Converts all data stored in the map file to Tile objects
        :return: Tile[] of tiles representing the map
        """
        res = []
        rownr = 0

        tmp = []
        arr = bytearray([])
        i = 0
        while i < len(self.mapLayout[0]):
            arr.append(self.PADDING_CHAR)
            i += 1
        tmp.append(arr)

        for x in self.mapLayout:
            tmp.append(x)
        self.mapLayout = tmp

        # print(len(self.mapLayout))
        # for x in self.mapLayout:
        #     print(str(x))
        while rownr < len(self.mapLayout):
            colnr = 0
            while colnr < len(self.mapLayout[rownr]) - 1:
                if self.mapLayout[rownr][colnr] != 32 and self.mapLayout[rownr][colnr] != 66 and self.mapLayout[rownr][colnr] != 120:
                    data = self.findTileData(self.mapLayout[rownr][colnr])
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
        param = self.getParamValue(lines[index])
        if param != "AUTO":
            self.mapWidth = int(float(param))
        index += 1

        # Read background stuff
        self.BACKGROUND_IMAGE = str(self.getParamValue(lines[index]))
        index += 1
        self.BACKGROUND_MUSIC = str(self.getParamValue(lines[index]))
        index += 1
        self.bgImage = tM.getImage(self.BACKGROUND_IMAGE, False)

        # Read player properties
        self.PLAYER_ACC = float(self.getParamValue(lines[index]))
        index += 1
        self.PLAYER_FRICTION = float(self.getParamValue(lines[index]))
        index += 1
        self.PLAYER_GRAV = float(self.getParamValue(lines[index]))
        index += 1
        self.PLAYER_JUMP = float(self.getParamValue(lines[index]))
        index += 1

        # Read enemy properties
        self.ENEMY_SPEED = float(self.getParamValue(lines[index]))
        index += 1

        # Read platform properties
        self.PLATFORM_SPEED = float(self.getParamValue(lines[index]))
        index += 1

        # Load maplayout
        self.mapLayout = self.getMapLayout(lines[index:])
        self.mapLayout = self.fillMapBottom(self.mapLayout)

        index += len(self.mapLayout) + 1

        # Load tile data
        self.tileData = self.getTileData(lines[index:])

        # print("Map initiated:")
        # print("Map name: " + self.mapName)
        # print("Width: " + str(self.mapWidth))
        # print("Height: " + str(self.mapHeight))
        # print("\nMapdata:")
        # for x in self.mapLayout:
        #     print(x)

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
        if self.mapWidth is None:
            self.mapWidth = len(data[0]) + 1
            print("Auto detected mapwidth set to: " + str(self.mapWidth))

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
            values.append(int(x))
        return values

    def findTileData(self, tid):
        temp = 0

        if len(self.tileData) > 0:
            # moving platform
            if tid == 77:
                temp = self.tileData[0]
                self.tileData = self.tileData[1:]

        return temp

    def getX(self, x):
        return settings.TILESIZE * x

    def getY(self, y):
        return settings.TILESIZE * y

    def fillMapBottom(self, data):
        rownr = len(data) - 2

        while rownr > 0:
            colnr = 0
            while colnr < len(data[rownr]):
                if data[rownr][colnr] == 32:
                    if (data[rownr + 1][colnr] == 66) or (data[rownr + 1][colnr] == 70):
                        data[rownr][colnr] = 70
                colnr += 1
            rownr -= 1

        rownr = 0

        while rownr < len(data):
            colnr = 0
            while colnr < len(data[rownr]):
                if data[rownr][colnr] == 70:
                    if (data[rownr][colnr - 1] not in air_tiles) \
                            and (data[rownr][colnr + 1] not in air_tiles
                            and (data[rownr - 1][colnr] not in air_tiles)):
                        data[rownr][colnr] = 120
                colnr += 1
            rownr += 1

        return data
