import pygame

class LevelBar:

    def __init__(self):
        self.posX = 300
        self.posY = 35
        self.totalLength = 400
        self.totalHeight = 25
        self.expColor = (255,0,0)
        self.outerBarColor = pygame.Color(90,90,90)
        self.fakeInnerColor = pygame.Color(20,20,20)
        self.inDel = 3

    def drawBar(self, screen, currPercentage):
        pygame.draw.rect(screen, self.outerBarColor, pygame.Rect(self.posX, self.posY, self.totalLength, self.totalHeight))
        pygame.draw.rect(screen, self.fakeInnerColor, pygame.Rect(self.posX + self.inDel, self.posY + self.inDel, self.totalLength - 2*self.inDel, self.totalHeight- 2*self.inDel))
        self.expColor = (int(255-255*(currPercentage)), int(255*(currPercentage)), 0)
        pygame.draw.rect(screen, pygame.Color(self.expColor), pygame.Rect(self.posX + self.inDel, self.posY + self.inDel, int(self.totalLength*(currPercentage)) - 2*self.inDel, self.totalHeight - 2*self.inDel))
