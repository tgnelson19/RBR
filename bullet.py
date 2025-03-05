import pygame
from math import sin, cos, sqrt

#Handles basic bullet statistics used during game calculation
class Bullet:

    def __init__(self, pX, pY, speed, direc, bRange, size, color, pierce, damage, currCrit, sW, sH, frameRate):
        self.posX = pX
        self.posY = pY
        self.iPosX = pX
        self.iPosY = pY
        self.sW = sW
        self.sH = sH
        self.speed = speed
        self.direc = direc
        self.size = size
        self.color = color
        self.bRange = bRange
        self.bPierce = pierce
        self.remFlag = False
        self.frameRate = frameRate
        self.damage = damage
        self.currCrit = currCrit


    def updateAndDrawBullet(self, screen):

        self.posX = self.posX + (self.speed*cos(self.direc)) * (120/self.frameRate)
        self.posY = self.posY - (self.speed*sin(self.direc)) * (120/self.frameRate)

        if(self.posX >= self.sW):
            self.posX = self.sW - 1
            self.remFlag = True
        elif(self.posX <= 0):
            self.posX = 1
            self.remFlag = True
        if(self.posY >= self.sH):
            self.posY = self.sH-1
            self.remFlag = True
        elif(self.posY <= 0):
            self.posY = 1
            self.remFlag = True

        pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.size, self.size))

        if(sqrt((abs(self.posX - self.iPosX) ** 2) + (abs(self.posY - self.iPosY) ** 2)) >= self.bRange): 
            self.remFlag = True