import pygame
from enemy import Enemy
from random import randint
from bullet import Bullet
from experienceBubble import ExperienceBubble
from math import atan, pi
from damageText import DamageText

#Wrangles the enemies and exp bubbles and damage texts (Pretty simple in concept)
class EnemyWrangler:    
    def __init__(self, tileSize, frameRate):
        self.enemyList = []
        self.experienceList = []
        self.damageTextList = []
        
        self.frameRate = frameRate

        self.noNoZone = None

        self.tileSize = tileSize

        self.stage = 1

        self.difficulty = .75 #Lower values makes an easier difficulty between 0-1

        self.enemySpeedMod = 1.02

        self.experienceStageMod = 1.1

        self.numOfEnemiesKilled = 0
        
        self.damageTextSizeBase = 40
        
        self.enemyBaseHP = 5

        self.enemyBaseExpValue = 10

        self.outOfMapDelta = 50

        self.playerHit = False

        self.expCount = 0

    def newNoNoZone(self, noNoZone, tileSize):
        self.noNoZone = noNoZone
        self.tileSize = tileSize

    def updateExperience(self, screen, tileSize, pAuraSpeed):
        for bubble in self.experienceList:
            bubble.updateBubble(screen, self.noNoZone, tileSize, pAuraSpeed)
            
    def updateDamageTexts(self, screen):
        for dText in self.damageTextList:
            dText.drawAndUpdateDamageText(screen)
            if (dText.deleteMe == True):
                self.damageTextList.remove(dText)
        

    def makeANewEnemy(self, type, w, h, oneIn):

        chance = randint(1, int(oneIn / (120/self.frameRate)))

        if(chance == 1):
            if (type == "crawler"):
                spawnSeed = randint(1,4)
                if (spawnSeed == 1):
                    x = randint(-self.outOfMapDelta, w + self.outOfMapDelta)
                    y = -self.outOfMapDelta
                elif (spawnSeed == 2):
                    x = randint(-self.outOfMapDelta, w + self.outOfMapDelta)
                    y = h + self.outOfMapDelta
                elif (spawnSeed == 3):
                    x = -self.outOfMapDelta
                    y = randint(-self.outOfMapDelta,h + self.outOfMapDelta)
                elif (spawnSeed == 4):
                    x = w + self.outOfMapDelta
                    y = randint(-self.outOfMapDelta, h + self.outOfMapDelta)

                enemyRange = randint(2, 15) / 10 #Randomly generated enemies for each stage

                self.enemyList.append(Enemy(x, y, (1+(self.stage-1)*self.enemySpeedMod) * (enemyRange/2), 
                                            int(self.tileSize / enemyRange), pygame.Color(255,0,0), 
                                            self.difficulty*((1+(self.stage-1)) / (enemyRange)), 
                                            (self.enemyBaseHP*self.stage) / (enemyRange),
                                            (self.enemyBaseExpValue * (self.stage)) / enemyRange, 
                                            self.frameRate))

    def updateEnemies(self, playerX, playerY):

        for enemy in self.enemyList:
            enemy.updateEnemy( playerX, playerY)
    
    def drawEnemies(self, screen):
        for enemy in self.enemyList:
            enemy.drawEnemy(screen)
        
    def hurtEnemies(self, liveRounds):
        for bullet in liveRounds:
            originX = bullet.posX + bullet.size/2
            originY = bullet.posY + bullet.size/2
            for eman in self.enemyList:
                if(originX + bullet.size/2 > eman.posX and originX - bullet.size/2< eman.posX + eman.size):
                    if(originY + bullet.size/2> eman.posY and originY - bullet.size/2< eman.posY + eman.size):
                        if (bullet not in eman.cantTouchMeList):
                            eman.cantTouchMeList.append(bullet)
                            bullet.bPierce -= 1
                            if (bullet.bPierce <= 0):
                                bullet.remFlag = True
                            eman.hp -= bullet.damage
                            if(bullet.currCrit):
                                currColor = pygame.Color(128,0,128)
                            else:
                                currColor = pygame.Color(200,120,0)
                            self.damageTextList.append(DamageText(eman.posX, eman.posY, self.damageTextSizeBase, currColor, bullet.damage, eman.size, self.frameRate))
                            if (eman.hp <= 0):
                                self.enemyList.remove(eman)
                                self.numOfEnemiesKilled += 1
                                self.experienceList.append(ExperienceBubble(eman.posX, eman.posY, eman.expValue*(self.stage*self.experienceStageMod), self.frameRate))

    def hurtPlayer(self, pX, pY, pSize, pDefense):
        for eman in self.enemyList:
            if(pX + pSize > eman.posX and pX < eman.posX + eman.size):
                if(pY + pSize > eman.posY and pY < eman.posY + eman.size):
                    self.playerHit = True
                    self.enemyList.remove(eman)
                    self.experienceList.append(ExperienceBubble(eman.posX, eman.posY, eman.expValue*(self.stage*self.experienceStageMod), self.frameRate))
                    trueDMG = eman.damage - pDefense
                    if (trueDMG < 0):
                        trueDMG = 0
                    self.damageTextList.append(DamageText(pX, pY, self.damageTextSizeBase, pygame.Color(200,100,0), trueDMG, self.tileSize, self.frameRate))
                    return trueDMG

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
