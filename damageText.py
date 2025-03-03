import pygame

class DamageText:

    def __init__(self, entX, entY, textBaseSize, color, value, framerate):
        self.posX = entX
        self.posY = entY
        self.color = color
        self.value = value
        self.textSize = textBaseSize
        self.lifetimeMax = framerate
        self.lifetime = framerate
        self.deleteMe = False

    def drawAndUpdateDamageText(self, screen):

        if (self.lifetime > self.lifetimeMax * (3/4)):
            self.lifetime -= 1
            self.textSize *= (1.01*self.lifetimeMax)
        if (self.lifetime > 0):
            self.lifetime -= 1
            self.textSize /= (1.01*self.lifetimeMax)
        if (self.lifetime <= 0):
            self.deleteMe = True

        font = pygame.font.Font("media/coolveticarg.otf", self.textSize)