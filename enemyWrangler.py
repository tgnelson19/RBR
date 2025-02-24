import pygame
from enemy import Enemy
from random import randint
from bullet import Bullet

class EnemyWrangler:    
    def __init__(self):
        self.enemyList = []

        self.numOfEnemiesKilled = 0

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