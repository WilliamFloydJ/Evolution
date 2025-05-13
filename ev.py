import pygame
import copy
import math
import random
from classes import vector2, vector3, pixel, cell, organism , action

# Initialize Pygame
pygame.init()

# Set window title
pygame.display.set_caption("Pixel Control Example")

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
    cel.pixel.rgb = (rgb.x, rgb.y, rgb.z)
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


# Your base resolution
width = 250
height = 156
base_surface = pygame.Surface((width, height))

# Your actual display window size (could be changed by the user)
screen_width = 1680
screen_height = 1050
screen = pygame.display.set_mode((screen_width, screen_height))

screen_scale = screen_width / width

blank_pixel = pixel((0,0,0))
celltype1 = cell(pixel((128,128,128),vector2(45,90)),action(2,0.05),action(0,0), 0.5, 0.05, action(4,0.02), 65, [])


def reset():
    global pixel_array,cellArr
    pixel_array = [[blank_pixel for col in range(width)] for row in range(height)]
    cell1 = cellType(celltype1,vector2(100,85))
    cell2 = cellType(celltype1,vector2(50,120))
    cell3 = cellType(celltype1,vector2(150,150))
    cellArr = [cell1,cell2,cell3]
    for cel in cellArr:
        position = cel.pixel.position
        pixel_array[position.y][position.x] = cel.pixel
    for y in range(height):
        for x in range(width):
            color = pixel_array[y][x].rgb
            base_surface.set_at((x, y), color)


milliwatts = 1.37

def simLoop():
    for cel in cellArr[:]:
        # Movement
        if percentChance(cel.movement.rate) and cel.energy > cel.movement.energy and allSpots(pixel_array,cel.pixel.position):
            newPos = allSpots(pixel_array,cel.pixel.position)
            position = cel.pixel.position
            pixel_array[position.y][position.x] = blank_pixel
            base_surface.set_at((position.x, position.y), (0,0,0))
            cel.energy -= cel.movement.energy
            cel.pixel.position = newPos
            position = cel.pixel.position
            pixel_array[position.y][position.x] = cel.pixel
            base_surface.set_at((position.x, position.y), cel.pixel.rgb)

        # Eating
        if percentChance(cel.eating.rate) and allSpots(pixel_array,cel.pixel.position) == False:
            pass

        # Growth
        if percentChance(cel.growth.rate) and allSpots(pixel_array,cel.pixel.position):
            newPos = allSpots(pixel_array,cel.pixel.position)
            base_surface.set_at((newPos.x, newPos.y), cel.pixel.rgb)
            cel.energy /= 2
            cel.energy -= cel.growth.energy
            newCel = copy.deepcopy(mutate(cel))
            newCel.pixel.position = newPos
            cellArr.append(newCel)

        energyGain = milliwatts * cel.absorption
        cel.energy += energyGain
        cel.energy = min(cel.energy,cel.energyMax)

        cel.energy -= cel.energyUse

        if cel.energy <= 0 or percentChance((cel.mutation + 0.001) / (50 - (cel.age / 100))):
            cellArr.remove(cel)
            position = cel.pixel.position
            pixel_array[position.y][position.x] = blank_pixel
            base_surface.set_at((position.x, position.y), (0,0,0))

        cel.age += 1


reset()
# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_a:
                length = len(cellArr)
                energy = 0
                totalEnergy = 0
                for cel in cellArr:
                    energy += cel.energy
                    totalEnergy += cel.age * (1.37 * cel.absorption)
                print(energy)
                print(totalEnergy) 
                print(round(energy/totalEnergy,2))

    simLoop()
    
    scaled_surface = pygame.transform.scale(base_surface, (screen_width, screen_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    

    # Keep the window open until the user closes it
    pygame.time.delay(1)

# Quit Pygame
pygame.quit()
