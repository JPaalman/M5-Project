import os
from game.resources.maps import mapManager
from game.resources.textures import textureManager
from game.resources.sounds import soundManager
from game import settings
import json

dirname = os.path.dirname(__file__)

texturemap = {
    33: "transparent.png",
    68: "lava.png",
    69: "android.png",
    112: "finish_flag.png",
    67: "flag.png",
    61: "gras-ground2.png",
    70: "ground2.png",
    99: "coin.png",
    45: "platform-middle.png",
    74: "jump_pad.png",
    256: "laser.png",
    90: "gras.png",
    120: "ground2.png",
    94: "spike_up.png",
    118: "spike_down.png",
    62: "spike_right.png",
    60: "spike_left.png",
    76: "laser.png"
}

uses_alpha = {33, 69, 112, 67, 99, 83, 74, 94, 118, 62, 60}


def getImageById(imgid):
    if imgid in texturemap:
        return textureManager.getImage(texturemap[imgid], imgid in uses_alpha)
    else:
        return textureManager.getImage("transparent.png", True)


def getImage(name, alpha):
    return textureManager.getImage(name, alpha)


def getMap(mapname):
    return mapManager.getMapLines(mapname)

def getSound(sound):
    return soundManager.getSound(sound)

def getHighscores():
    filename = os.path.join(dirname, settings.highscores_file)
    file_object = open(filename, )

    mp = {}

    try:
        1
        mp = json.load(file_object)
    except json.decoder.JSONDecodeError:
        file_object.close()
        print("file closed in except")

    file_object.close()

    return mp


def writeHighscores(obj):
    filename = os.path.join(dirname, settings.highscores_file)
    file_object = open(filename, "w")

    index = 0
    tmp = []
    while index < len(settings.PLAYLIST):
        tmp.append(settings.PLAYLIST[index][0])
        index += 1

    for x in tmp:
        if x not in obj.keys():
            obj[x] = []

    rm = []
    for x in obj.keys():
        if x not in tmp:
            rm.append(x)

    for x in rm:
        obj.pop(x, None)

    json.dump(obj, file_object)
    file_object.close()
    print("end2")