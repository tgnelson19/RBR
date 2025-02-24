import pygame
from enemy import Enemy
from random import randint

class EnemyWrangler:    
    def __init__(self):
        self.enemyList = []

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

    def updateEnemies(self, screen, playerX, playerY, playerSize):
        for enemy in self.enemyList:
            enemy.updateAndDrawEnemy(screen, playerX, playerY, playerSize)

