import pygame
from math import floor, ceil, atan, pi
from bullet import Bullet

class Character:

    def __init__(self, defX, defY):
        self.positionX = defX
        self.positionY = defY
        self.playerSpeed = 3
        self.playerSize = 25
        self.playerColor = pygame.Color(0,0,255)

        self.noNoZone = None

        self.liveRounds = []
        self.attackCooldownStat = 20
        self.attackCooldownTimer = 0 #Number of frames before next bullet can be fired (Yes, I know, I don't care)
        self.bulletSpeed = 5
        self.bulletRange = 200
        self.bulletSize = 10
        self.bulletColor = pygame.Color(125,125,125)

    def newNoNoZone(self, noNoZone, tileSize):
        self.noNoZone = noNoZone
        self.tileSize = tileSize

    def handlingBullets(self, screen, mouseDown, mouseX, mouseY):

        if (self.attackCooldownTimer == 0 and mouseDown):

            self.attackCooldownTimer = self.attackCooldownStat
            originX = self.positionX + (self.playerSize / 2)
            originY = self.positionY + (self.playerSize / 2)

            deltaX = mouseX - originX
            deltaY = mouseY - originY

            direction = 0

            if (deltaX == 0):
                if(deltaY > 0):
                    direction = 0
                else:
                    direction = -pi
            else:
                
                if(deltaX > 0):

                    direction = -atan(deltaY/deltaX)
                else:
                    deltaX = abs(mouseX - originX)

                    direction = atan(deltaY/deltaX) + pi

            self.liveRounds.append(Bullet(originX, originY, self.bulletSpeed, direction, self.bulletRange, self.bulletSize, self.bulletColor))

        elif(self.attackCooldownTimer > 0):
            self.attackCooldownTimer -= 1

        for bullet in self.liveRounds:
            bullet.updateAndDrawBullet(screen)

            currX = bullet.posX / self.tileSize #Current Position in tiles
            currY = bullet.posY / self.tileSize #Current Position in tiles

            if(self.noNoZone[floor(currX)][floor(currY)] == "wall" or self.noNoZone[ceil(currX)][floor(currY)] == "wall" or self.noNoZone[floor(currX)][ceil(currY)] == "wall" or self.noNoZone[ceil(currX)][ceil(currY)] == "wall"):
                self.liveRounds.remove(bullet)
            elif (bullet.remFlag == True):
                self.liveRounds.remove(bullet)


    def moveAndDrawPlayer(self, screen, keysDown):

        doubleChecker = 0
        scalar = 1

        for i in keysDown:
            if i:
                doubleChecker += 1

        if doubleChecker == 2:
            scalar = 0.707

        dX, dY = 0,0

        if keysDown[0]:
            dY -= 1 * scalar
        if keysDown[1]:
            dX -= 1 * scalar
        if keysDown[2]:
            dY += 1 * scalar
        if keysDown[3]:
            dX += 1 * scalar

        currX = self.positionX / self.tileSize #Current Position
        currY = self.positionY / self.tileSize #Current Position

        potNewX = (self.positionX + (dX * self.playerSpeed)) / self.tileSize #Exact float X coordinate desired
        potNewY = (self.positionY + (dY * self.playerSpeed)) / self.tileSize #Exact float Y coordinate desired

        noMoveX = False
        noMoveY = False

        if (dX < 0):
            if (self.noNoZone[floor(potNewX)][floor(currY)] == "wall"):
                self.positionX = ceil(potNewX) * self.tileSize
                noMoveX = True
        if (dX > 0):
            if (self.noNoZone[ceil(potNewX)][floor(currY)] == "wall"):
                self.positionX = floor(potNewX) * self.tileSize
                noMoveX = True
        if (dY < 0):
            if (self.noNoZone[floor(currX)][floor(potNewY)] == "wall"):
                self.positionY = ceil(potNewY) * self.tileSize
                noMoveY = True
        if (dY > 0):
            if (self.noNoZone[floor(currX)][ceil(potNewY)] == "wall"):
                self.positionY = floor(potNewY) * self.tileSize
                noMoveY = True

        if (not noMoveX):
            self.positionX += dX * self.playerSpeed

        if (not noMoveY):
            self.positionY += dY * self.playerSpeed

        pygame.draw.rect(screen, self.playerColor, pygame.Rect(self.positionX, self.positionY, self.playerSize, self.playerSize))
