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
                if(spawnSeed == 1):
                    x = w/2
                    y = 0
                if(spawnSeed == 2):
                    x = w
                    y = h/2
                if(spawnSeed == 3):
                    x = w/2
                    y = h
                if(spawnSeed == 4):
                    x = 0
                    y = h/2
                
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