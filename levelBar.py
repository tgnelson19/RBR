import pygame

#When reaches full, give a level, located in top right corner
class LevelBar:

    def __init__(self, sW, sH, tileSize):
        
        self.sW = sW
        self.sH = sH
        self.tileSize = tileSize

        self.totalLength = int(sW / 3.2)
        self.totalHeight = int(tileSize*(3/5))
        self.posX = self.sW - self.totalLength - tileSize
        self.posY = int(self.tileSize/5)

        self.expColor = (255,0,0)
        self.outerBarColor = pygame.Color(70,70,70)
        self.fakeInnerColor = pygame.Color(20,20,20)
        self.inDel = 3

    def drawBar(self, screen, currPercentage):
        pygame.draw.rect(screen, self.outerBarColor, pygame.Rect(self.posX, self.posY, self.totalLength, self.totalHeight))
        pygame.draw.rect(screen, self.fakeInnerColor, pygame.Rect(self.posX + self.inDel, self.posY + self.inDel, self.totalLength - 2*self.inDel, self.totalHeight- 2*self.inDel))
        self.expColor = (int(255-255*(currPercentage)), int(255*(currPercentage)), 0)
        pygame.draw.rect(screen, pygame.Color(self.expColor), pygame.Rect(self.posX + self.inDel, self.posY + self.inDel, int(self.totalLength*(currPercentage)) - 2*self.inDel, self.totalHeight - 2*self.inDel))
