import game.map.map as map
import settings
import os

map_obj = map.Map(settings.LEVEL_1)
mapBytes = map_obj.getMapLayout(map_obj.cleanLines(map_obj.rawMapLines)[11:])

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, settings.LEVEL_1)

file_object = open("dump.txt", 'w')
for x in mapBytes:
    print(str(x))
    file_object.write(bytes(x).decode("ascii")[:-1] + "\n")
