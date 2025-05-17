import pygame
import copy
from functions import percentChance, checkSpot, allSpots, mutate, cellType, checkArr
from classes import Color, vector2, vector3, pixel, cell, organism , action

# Initialize Pygame
pygame.init()

# Set window title
pygame.display.set_caption("Pixel Control Example")

# Your base resolution
width = 250
height = 156
base_surface = pygame.Surface((width, height))

# Your actual display window size (could be changed by the user)
screen_width = 1680
screen_height = 1050
screen = pygame.display.set_mode((screen_width, screen_height))

screen_scale = screen_width / width

blank_pixel = pixel(Color(0,0,0))
celltype1 = cell(pixel(Color(128,128,128),vector2(45,90)),action(2,0.05),action(0,0), 0.5, 0.05, action(4,0.02), 65, [])


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
            newPos = newPos if newPos else vector2(0,0)
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
            newPos = newPos if newPos else vector2(0,0)
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
