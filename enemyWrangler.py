import pygame
from enemy import Enemy
from random import randint
from bullet import Bullet
from experienceBubble import ExperienceBubble
from math import atan, pi

class EnemyWrangler:    
    def __init__(self):
        self.enemyList = []
        self.experienceList = []

        self.noNoZone = None

        self.numOfEnemiesKilled = 0

        self.dead = False

        self.expCount = 0

    def newNoNoZone(self, noNoZone, tileSize):
        self.noNoZone = noNoZone
        self.tileSize = tileSize

    def updateExperience(self, screen, tileSize, pAuraSpeed):
        for bubble in self.experienceList:
            bubble.updateBubble(screen, self.noNoZone, tileSize, pAuraSpeed)
        

    def makeANewEnemy(self, type, w, h, oneIn):

        chance = randint(1, oneIn)

        if(chance == 1):
            if (type == "crawler"):
                spawnSeed = randint(1,4)
                if (spawnSeed == 1):
                    x = randint(1,w - 1)
                    y = 1
                elif (spawnSeed == 2):
                    x = randint(1,w - 1)
                    y = h - 1
                elif (spawnSeed == 3):
                    x = 0
                    y = randint(1,h - 1)
                elif (spawnSeed == 4):
                    x = w - 1
                    y = randint(1,h - 1)
                self.enemyList.append(Enemy(x, y, 1, 25, pygame.Color(255,0,0), 1))

    def updateEnemies(self, screen, playerX, playerY):

        for enemy in self.enemyList:
            enemy.updateAndDrawEnemy(screen, playerX, playerY)
        
        

    def hurtEnemies(self, liveRounds):
        for bullet in liveRounds:
            originX = bullet.posX + bullet.size/2
            originY = bullet.posY + bullet.size/2
            for eman in self.enemyList:

                if(originX + bullet.size/2 > eman.posX and originX - bullet.size/2< eman.posX + eman.size):
                    if(originY + bullet.size/2> eman.posY and originY - bullet.size/2< eman.posY + eman.size):
                        bullet.remFlag = True
                        self.enemyList.remove(eman)
                        self.numOfEnemiesKilled += 1
                        self.experienceList.append(ExperienceBubble(eman.posX, eman.posY, 10))

    def hurtPlayer(self, pX, pY, pSize):
        for eman in self.enemyList:
            if(pX + pSize > eman.posX and pX < eman.posX + eman.size):
                if(pY + pSize > eman.posY and pY < eman.posY + eman.size):
                    self.dead = True

    def expForPlayer(self, pX, pY, pSize, pAura):
        for bubble in self.experienceList:
            if(pX + pSize > bubble.posX and pX < bubble.posX + bubble.size):
                if(pY + pSize > bubble.posY and pY < bubble.posY + bubble.size):
                    self.expCount += bubble.value
                    self.experienceList.remove(bubble)

            

            if(pX + pSize + pAura > bubble.posX and pX - pAura < bubble.posX + bubble.size):
                if(pY + pSize + pAura > bubble.posY and pY - pAura < bubble.posY + bubble.size):

                    bubble.naturalSpawn = False
                    
                    originX = pX + pSize/2
                    originY = pY + pSize/2

                    #This is direct center x, y of player

                    deltaX = bubble.posX - originX
                    deltaY = bubble.posY - originY

                    #This is direct xhat, yhat vector towards player

                    if (deltaX == 0):
                        if(deltaY > 0):
                            bubble.direction = pi/2
                        else:
                            bubble.direction = -pi/2
                    else:
                        
                        if(deltaX > 0):

                            bubble.direction = atan(deltaY/deltaX)
                        else:
                            deltaX = abs(bubble.posX - originX)

                            bubble.direction = -atan(deltaY/deltaX) + pi
                else:
                    bubble.naturalSpawn = True
            else:
                bubble.naturalSpawn = True
