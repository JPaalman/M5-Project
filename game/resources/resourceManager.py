import os
from game.resources.maps import mapManager
from game.resources.textures import textureManager
from game.resources.sounds import soundManager
from game import settings as s
import json

dirname = os.path.dirname(__file__)

texturemap = {
    33: {s.NORMAL: "transparent.png"},
    68: {s.NORMAL: "lava.png"},
    69: {s.NORMAL: "android.png"},
    112: {s.NORMAL: "finish_flag.png"},
    67: {s.NORMAL: "flag.png"},
    61: {s.NORMAL: "gras-ground2.png", s.JUNGLE: "junglegrass.png"},
    70: {s.NORMAL: "ground2.png", s.JUNGLE: "junglefiller.png"},
    99: {s.NORMAL: "coin.png"},
    45: {s.NORMAL: "platform-middle.png", s.JUNGLE: "jungleplatform.png"},
    74: {s.NORMAL: "jump_pad.png"},
    256: {s.NORMAL: "laser.png"},
    90: {s.NORMAL: "gras.png"},
    120: {s.NORMAL: "ground2.png", s.JUNGLE: "junglefiller.png"},
    94: {s.NORMAL: "spike_up.png"},
    118: {s.NORMAL: "spike_down.png"},
    62: {s.NORMAL: "spike_right.png"},
    60: {s.NORMAL: "spike_left.png"},
    76: {s.NORMAL: "laser.png"}
}

uses_alpha = {33, 69, 112, 67, 99, 83, 74, 94, 118, 62, 60, 45}


def getImageById(imgid, style):
    if imgid in texturemap:
        alpha = imgid in uses_alpha
        try:
            return textureManager.getImage(texturemap.get(imgid, {}).get(style), alpha)
        except:
            return textureManager.getImage(texturemap[imgid][s.NORMAL], alpha)
    else:
        return textureManager.getImage("transparent.png", True)

def getImage(name, alpha):
    return textureManager.getImage(name, alpha)

def getMap(mapname):
    return mapManager.getMapLines(mapname)

def getSound(sound):
    return soundManager.getSound(sound)

def loadMusic(sound):
    soundManager.loadMusic(sound)

def getHighscores():
    filename = os.path.join(dirname, s.highscores_file)
    file_object = open(filename, )

    mp = json.load(file_object)

    file_object.close()

    return mp


def writeHighscores(obj):
    filename = os.path.join(dirname, s.highscores_file)
    file_object = open(filename, "w")

    index = 0
    tmp = []
    while index < len(s.PLAYLIST):
        tmp.append(s.PLAYLIST[index][0])
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