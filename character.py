import pygame
from math import floor, ceil, atan, pi
from bullet import Bullet
from levelBar import LevelBar
from charHPBar import CharHPBar

class Character:

    def __init__(self, defX, defY, tileSize, numTX, numTY, sW, sH, frameRate):
        self.positionX = defX
        self.positionY = defY
        self.playerSpeed = 3.5
        self.playerSize = tileSize
        self.tileSize = tileSize
        self.numTX = numTX
        self.numTY = numTY
        self.sW = sW
        self.sH = sH
        self.frameRate = frameRate
        
        self.playerColor = pygame.Color(0,0,255)

        self.noNoZone = None

        self.liveRounds = [] #Storage of every single round on the screen
        self.projectileCount = 1
        self.multiBallLevelMod = 5
        self.azimuthalProjectileAngle = 0
        self.attackCooldownStat = 20
        self.attackCooldownTimer = 0 #Number of frames before next bullet can be fired (Yes, I know, I don't care)
        self.bulletSpeed = 5
        self.bulletRange = 200
        self.bulletSize = 10
        self.bulletColor = pygame.Color(125,125,125)
        self.aura = 50
        self.auraSpeed = 4
        self.levelMod = 1.1
        self.damage = 1
        self.healthPoints = 10
        self.maxHealthPoints = 10
        self.bulletPierce = 1

        self.currentLevel = 0
        self.expNeededForNextLevel = 50
        self.baseExpNeededForNextLevel = 50
        self.levelScaleIncreaseFunction = 1.2
        self.levelBar = LevelBar(self.sW, self.sH, self.tileSize)
        self.healthBar = CharHPBar(self.sW, self.sH, self.tileSize)

    def newNoNoZone(self, noNoZone, tileSize):
        self.noNoZone = noNoZone
        self.tileSize = tileSize

    def resetCharStats(self):
        self.liveRounds = [] #Storage of every single round on the screen
        self.projectileCount = 1
        self.azimuthalProjectileAngle = pi/16
        self.playerSpeed = 3.5
        self.attackCooldownStat = 20
        self.attackCooldownTimer = 0 #Number of frames before next bullet can be fired (Yes, I know, I don't care)
        self.bulletSpeed = 5
        self.bulletRange = self.sH/4
        self.bulletSize = self.tileSize/2
        self.bulletColor = pygame.Color(125,125,125)
        self.aura = self.tileSize*2
        self.auraSpeed = 4
        self.damage = 1
        self.healthPoints = 10
        self.bulletPierce = 1
        self.defense = 0

    def levelUpStatsBasic(self):

        if (self.attackCooldownStat > 1):
            self.attackCooldownStat = int(self.attackCooldownStat / self.levelMod)
        
        if (self.bulletSpeed < 50):
            self.bulletSpeed = (self.bulletSpeed* self.levelMod)

        if (self.playerSpeed < 50):
            self.playerSpeed *= (1+(self.levelMod-1)/3)
        
        if (self.bulletRange < 1000):
            self.bulletRange = (self.bulletRange*self.levelMod)

        if(self.currentLevel % self.multiBallLevelMod == 0):
            self.projectileCount += 1
            
        self.damage += 0.1
        self.bulletPierce += 0
        self.defense += 0


    def handlingBullets(self, screen, mouseDown, mouseX, mouseY):

        if (self.attackCooldownTimer <= 0 and mouseDown):

            self.attackCooldownTimer = self.attackCooldownStat

            for bNum in range(0,self.projectileCount):
                
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

                if(self.projectileCount != 1):

                    dirDelta = -(self.azimuthalProjectileAngle / 2)

                    direction += dirDelta + bNum*(self.azimuthalProjectileAngle / (self.projectileCount-1))

                self.liveRounds.append(Bullet(originX - (self.bulletSize / 2), originY - (self.bulletSize / 2), self.bulletSpeed, direction, self.bulletRange, self.bulletSize, self.bulletColor, self.bulletPierce, self.sW, self.sH, self.frameRate))

        elif(self.attackCooldownTimer > 0):
            self.attackCooldownTimer -= 1 * (120/self.frameRate)

        for bullet in self.liveRounds:
            bullet.updateAndDrawBullet(screen)

            currX = bullet.posX / self.tileSize #Current Position in tiles
            currY = bullet.posY / self.tileSize #Current Position in tiles

            try:

                if( self.noNoZone[int(currX)][int(currY)] == "wall"):
                    self.liveRounds.remove(bullet)
                elif (bullet.remFlag == True):
                    self.liveRounds.remove(bullet)

            except IndexError:
                self.liveRounds.remove(bullet)

    def shareExpAndHP(self, screen, exp):

        self.healthBar.drawBar(screen, self.healthPoints/self.maxHealthPoints)

        percentage = exp/self.expNeededForNextLevel

        if (exp >= self.expNeededForNextLevel):
            self.currentLevel += 1
            self.expNeededForNextLevel *= self.levelScaleIncreaseFunction
            self.levelBar.drawBar(screen, 1)
            self.levelUpStatsBasic()
            return 0
        else:
            self.levelBar.drawBar(screen, percentage)
            return exp
        


    def moveAndDrawPlayer(self, screen, keysDown):

        doubleChecker = 0
        scalar = 1

        playerDecision = "no"

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

        potNewX = (self.positionX + (dX * self.playerSpeed) * (120/self.frameRate)) / self.tileSize #Exact float X coordinate desired
        potNewY = (self.positionY + (dY * self.playerSpeed) * (120/self.frameRate)) / self.tileSize #Exact float Y coordinate desired

        if (potNewX < 0):
            playerDecision = "left"
            noMoveX = True
            noMoveY = True
        elif (potNewY < 0):
            playerDecision = "top"
            noMoveX = True
            noMoveY = True
        elif (potNewX > self.numTX - 1):
            playerDecision = "right"
            noMoveX = True
            noMoveY = True
        elif (potNewY > self.numTY - 1):
            playerDecision = "bottom"
            noMoveX = True
            noMoveY = True
        else:
            noMoveX = False
            noMoveY = False

            try:

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
            except IndexError:
                currX = 0

            if (not noMoveX):
                self.positionX += (dX * self.playerSpeed) * (120/self.frameRate)

            if (not noMoveY):
                self.positionY += (dY * self.playerSpeed) * (120/self.frameRate)

        #Shows Aura
        #pygame.draw.rect(screen, pygame.Color(0,100,0), pygame.Rect(self.positionX - self.aura, self.positionY - self.aura, self.playerSize + 2*self.aura, self.playerSize +2*self.aura))

        pygame.draw.rect(screen, self.playerColor, pygame.Rect(self.positionX, self.positionY, self.playerSize, self.playerSize))

        return playerDecision
