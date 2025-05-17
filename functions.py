import math
import random
import copy

from classes import Color,vector2, vector3, pixel, cell, organism , action

def percentChance(chance):
    num = random.random()
    return chance > num

def checkSpot(array, position):
    pos1 = array[position.y][position.x]
    return pos1.rgb == (0,0,0)

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

mutateAmount = 0.1
def mutate(cel : cell):
    rgb = vector3(cel.pixel.rgb[0],cel.pixel.rgb[1],cel.pixel.rgb[2])
    if percentChance(cel.mutation):
        row = 0
        times = 0
        amountTimes = 1
        for val in vars(cel).values():
            amount = 0
            if isinstance(val , action):
                if percentChance(0.5):
                    val.energy += mutateAmount
                    val.rate += mutateAmount
                    amount += 1
                else:
                    val.energy -= mutateAmount
                    val.rate -= mutateAmount
                    amount -= 1
            elif isinstance(val, list) == False and isinstance(val, pixel) == False:
                if percentChance(0.5):
                    val += mutateAmount
                    amount += 1
                else:
                    val -= mutateAmount
                    amount -= 1
            else:
                continue
            rgb.arrayAdd(row - (times * 3),amount * amountTimes)
            row += 1
            if row % 3 == 0:
                times += 1
                amountTimes += 3
    cel.pixel.rgb = Color(rgb.x, rgb.y, rgb.z)
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