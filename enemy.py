import pygame
from math import pi, atan, cos, sin

class Enemy:

    def __init__(self, posX, posY, speed, size, color, damage):
        self.posX = posX
        self.posY = posY
        self.speed = speed
        self.size = size
        self.color = color
        self.damage = damage
        self.direction = 0


    def updateAndDrawEnemy(self, screen, playerX, playerY):
        
        #Logic for a basic crawler enemy (All anyone wants to fight anyway these days, brainrot...)
        
        originX = playerX
        originY = playerY

        #This is direct center x, y of player

        deltaX = self.posX - originX
        deltaY = self.posY - originY

        #This is direct xhat, yhat vector towards player

        if (deltaX == 0):
            if(deltaY > 0):
                    self.direction = -pi/2
            else:
                self.direction = pi/2
        else:
            
            if(deltaX > 0):

                self.direction = atan(deltaY/deltaX)
            else:
                deltaX = abs(self.posX - originX)

                self.direction = -atan(deltaY/deltaX) + pi

        self.posX -= self.speed*cos(self.direction)
        self.posY -= self.speed*sin(self.direction)

        pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.size, self.size))

