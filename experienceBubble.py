from random import randint
from math import cos, sin, floor, ceil
import pygame

#Lil' bubble that chases player when in aura and helps level up
class ExperienceBubble:    
    def __init__(self, oX, oY, value, frameRate):
        self.size = 20
        self.color = pygame.Color(0,200,0)
        self.oX = oX
        self.posX = oX
        self.oY = oY
        self.posY = oY
        self.value = value
        self.direction = randint(0,360) * 0.0174533
        self.speedSpan = 40
        self.speed = 2.5
        self.naturalSpawn = True
        self.frameRate = frameRate

    def updateBubble(self, screen, noNoZone, tileSize, pAuraSpeed):

        if(self.naturalSpawn):

            if (self.speedSpan > 0):
                self.speedSpan -= 1 * (120/self.frameRate)
                
            if (self.speedSpan <= 0):
                self.speed = 0
            elif(self.speedSpan < 20):
                self.speed = 1.25

            potNewX = (self.posX - self.speed*cos(self.direction) * (120/self.frameRate)) / tileSize #Exact float X coordinate desired
            potNewY = (self.posY - self.speed*sin(self.direction) * (120/self.frameRate)) / tileSize #Exact float Y coordinate desired

            noMoveX = False
            noMoveY = False

            currX = self.posX / tileSize #Current Position
            currY = self.posY / tileSize #Current Position

            try:

                if (-cos(self.direction) < 0):
                    if (noNoZone[floor(potNewX)][floor(currY)] == "wall"):
                        self.positionX = ceil(potNewX) * tileSize
                        noMoveX = True
                if (-cos(self.direction) > 0):
                    if (noNoZone[ceil(potNewX)][floor(currY)] == "wall"):
                        self.positionX = floor(potNewX) * tileSize
                        noMoveX = True
                if (-sin(self.direction) < 0):
                    if (noNoZone[floor(currX)][floor(potNewY)] == "wall"):
                        self.positionY = ceil(potNewY) * tileSize
                        noMoveY = True
                if (-sin(self.direction) > 0):
                    if (noNoZone[floor(currX)][ceil(potNewY)] == "wall"):
                        self.positionY = floor(potNewY) * tileSize
                        noMoveY = True

                if (not noMoveX):
                    self.posX -= self.speed*cos(self.direction) * (120/self.frameRate)

                if (not noMoveY):
                    self.posY -= self.speed*sin(self.direction) * (120/self.frameRate)
                    
            except IndexError:
                self.speed = 0
                self.dir = 0

        else:
            self.posX -= pAuraSpeed*cos(self.direction) * (120/self.frameRate)
            self.posY -= pAuraSpeed*sin(self.direction) * (120/self.frameRate)  


        pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.size, self.size))