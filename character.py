import pygame

class Character:

    def __init__(self, defX, defY):
        self.positionX = defX
        self.positionY = defY
        self.playerSpeed = 3
        self.playerSize = 20
        self.playerColor = pygame.Color(0,0,255)


    def movePlayer(self, screen, keysDown):

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

        self.positionX += dX * self.playerSpeed
        self.positionY += dY * self.playerSpeed

        pygame.draw.rect(screen, self.playerColor, pygame.Rect(self.positionX, self.positionY, self.playerSize, self.playerSize))