import game.map.map as map
import settings
import os

map_obj = map.Map(settings.LEVEL_1)
mapBytes = map_obj.getMapLayout(map_obj.cleanLines(map_obj.rawMapLines)[8:])

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, settings.LEVEL_1)

file_object = open("dump.txt", 'w')
for x in mapBytes:
    file_object.write(x.decode("ascii")[:-1] + "\n")
