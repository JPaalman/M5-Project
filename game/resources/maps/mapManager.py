import os


def getMapLines(mapname):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, mapname)

    file_object = open(filename, )
    return file_object.readlines()