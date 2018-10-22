import os

class Map:

    def __init__(self, mname):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, mname)
        file_object = open(filename, 'r')
        self.rawMapLines = file_object.readlines()
        self.initMap(self.rawMapLines)

    def getMap(self):
        # TODO add direction argument for moving the view of the map
        return self.mapLayout

    def initMap(self, lines):

        lines = self.cleanLines(lines)

        mapName = ""
        mapHeight = 0
        mapWidth = 0
        mapLayout = []

        index = 0;

        # Read map name
        mapName = self.getParamValue(lines[index])
        index += 1

        # Read map height
        mapHeight = int(float(self.getParamValue(lines[index])))
        index += 1

        # Read map width
        mapWidth = int(float(self.getParamValue(lines[index])))
        index += 1

        # Load maplayout
        mapLayout = self.getMapLayout(lines[index:])


        # Load tile data
        # TODO implement

        # Put values into instance variables
        self.mapHeight = mapHeight
        self.mapWidth = mapWidth
        self.mapLayout = mapLayout
        self.mapName = mapName

        print("Map initiated:")
        print("Map name: " + self.mapName)
        print("Width: " + str(self.mapWidth))
        print("Height: " + str(self.mapHeight))
        print("\nMapdata:")
        for x in mapLayout:
            print(x)

    def cleanLines(self, list):

        for x in list:
            x.rstrip()

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
            if (str(x) == "!MAPEND"):
                return res
            res.append(bytearray(x, "ascii"))
        return res