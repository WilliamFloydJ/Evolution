import math
import random
import copy

from classes import Color,vector2, vector3, pixel, cell, organism , action

def percentChance(chance):
    num = random.random()
    return chance > num

def checkSpot(array, position):
    if position.y > len(array) or position.x > len(array[0]):
        pos1 = array[position.y][position.x]
        return pos1.rgb == (0,0,0)
    else:
        return True
    
spots = [vector2(-1,-1),vector2(0,-1),vector2(1,-1),vector2(-1,0),vector2(1,0),vector2(-1,1),vector2(0,1),vector2(1,1)]
def allSpots(array, position: vector2):
    posSpots = spots.copy()
    for i in range(8):
        randi = random.randint(0,len(posSpots)-1)
        newPos = position.add(posSpots[randi])
        if checkSpot(array,newPos):
            return newPos
        else:
            posSpots.pop(randi)  
    return False

mutateAmount = 0.01
def mutate(cel : cell):
    rgb = vector3(cel.pixel.rgb[0],cel.pixel.rgb[1],cel.pixel.rgb[2])
    for key in vars(cel):
        keyType = type(cel[key]).__name__
        if keyType in ["list","pixle"]: continue
        if percentChance(cel.mutation):
            mutKeys = [key]
            for subKey in vars(cel[key]):
                mutKeys.append(subKey)
            newKey = ".".join(mutKeys)
            cel.mutate(newKey)
    cel.updateUse()
    return cel

def cellType(type: cell, position):
    cel = copy.deepcopy(type)
    cel.pixel.position = position
    return cel

def checkArr(array, position: vector2):
    for cel in array:
        if cel.pixel.position == position:
            return True
    return False

def get_nested(d, key):
    keys = key.split(".")
    for k in keys:
        d = d[k]
    return d

def add_nested_value(data, key_path, value):
    keys = key_path.split(".")
    for key in keys[:-1]:
        data = data.setdefault(key, {})  # create nested dicts if missing
    data[keys[-1]] += value