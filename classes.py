import pygame

Color = pygame.Color

class vector3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y 
        self.z = z

    def arrayAdd(self,index,amount):
        if index == 0:
            self.x += amount
        elif index == 1:
            self.y += amount
        elif index == 2:
            self.z += amount

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

class vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y 

    def add(self,vector):
        return vector2(self.x + vector.x , self.y + vector.y)

    def __str__(self):
        return f"({self.x},{self.y})"


class pixel:
    def __init__(self,rgb: Color = Color(0,0,0), position: vector2 = vector2(0,0)):
        self.rgb = rgb
        self.position = position
    
    def __str__(self):
        return f"({self.rgb[0]},{self.rgb[1]},{self.rgb[2]})"

class action:
    def __init__(self, energy , rate):
        self.energy = energy
        self.rate = rate
        pass

    def __str__(self):
        return f"({self.energy},{self.rate})"

class cell:
    def __init__(self,pixel : pixel, movement: action, eating: action, absorption, mutation, growth: action, energyMax, actionList: list):
        self.pixel = pixel
        self.movement = movement
        self.eating = eating
        self.absorption = absorption
        self.mutation = mutation
        self.growth = growth
        self.energy = energyMax
        self.energyMax = energyMax
        self.actionList = actionList
        self.age = 0
        self.energyUse = (movement.rate + eating.rate + growth.rate + (energyMax / 200)) / 2
    
    def updateUse(self):
        self.energyUse = (self.movement.rate + self.eating.rate + self.growth.rate + (self.energyMax / 200)) / 2

    def __str__(self):
        return f"{self.movement},{self.eating},{self.absorption},{self.mutation},{self.growth},{self.energyMax}"
        

class organism:
    def __init__(self,cells : list):
        self.cells = cells