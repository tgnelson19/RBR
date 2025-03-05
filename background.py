import pygame

class Background:

    def __init__(self, w, h, tileSize, bckColor):

        self.sW = w
        self.sH = h

        self.tileSize = tileSize
        self.doorRad = 3

        self.numHori = int(self.sW/self.tileSize)
        self.numVerti = int(self.sH/self.tileSize)

        self.tileTypes = {
            "wall": pygame.Color(90,90,90), 
            "default" : bckColor
            }

        self.currentLayout = [[0 for _ in range(self.numVerti)] for _ in range(self.numHori)]


    def makeDefaultRoom(self):

        for i in range(self.numHori):
            for j in range(self.numVerti):
                    if (i==0) or (j==0) or (i == self.numHori - 1) or (j == self.numVerti - 1):
                        self.currentLayout[i][j] = "wall"
                    else:
                        self.currentLayout[i][j] = "default"

    def openDoors(self):
        for i in range(self.numHori):
            for j in range(self.numVerti):
                if(i == 0 and j > (int(self.numVerti / 2) - self.doorRad) and j < (int(self.numVerti / 2) + self.doorRad)):
                    self.currentLayout[i][j] = "default"
                if(i == self.numHori - 1 and j > (int(self.numVerti / 2) - self.doorRad) and j < (int(self.numVerti / 2) + self.doorRad)):
                    self.currentLayout[i][j] = "default"
                if(j == 0 and i > (int(self.numHori / 2) - self.doorRad) and i < (int(self.numHori / 2) + self.doorRad) ):
                    self.currentLayout[i][j] = "default"
                if(j == self.numVerti -1  and i > (int(self.numHori / 2) - self.doorRad)  and i < (int(self.numHori / 2) + self.doorRad) ):
                    self.currentLayout[i][j] = "default"
        
    def displayCurrentWalls(self, screen, backColor):
        for i in range(self.numHori):
            for j in range(self.numVerti):
                if (self.currentLayout[i][j] == "wall"):
                    pygame.draw.rect(screen, self.tileTypes[self.currentLayout[i][j]], pygame.Rect(i*self.tileSize, j*self.tileSize, self.tileSize, self.tileSize))
    
    def displayCurrentDefaults(self, screen, backColor):
        
        self.tileTypes["default"] = backColor

        for i in range(self.numHori):
            for j in range(self.numVerti):
                if (self.currentLayout[i][j] == "default"):
                    pygame.draw.rect(screen, self.tileTypes[self.currentLayout[i][j]], pygame.Rect(i*self.tileSize, j*self.tileSize, self.tileSize, self.tileSize))