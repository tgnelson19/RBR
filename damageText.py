import pygame

class DamageText:

    def __init__(self, entX, entY, textBaseSize, color, value, framerate):
        self.posX = entX
        self.posY = entY
        self.color = color
        self.value = value
        self.textSize = textBaseSize
        self.lifetimeMax = framerate
        self.frameRate = framerate
        self.lifetime = framerate
        self.deleteMe = False
        self.deltaVal = 10
        self.font = pygame.font.Font("media/coolveticarg.otf", int(self.textSize))

    def drawAndUpdateDamageText(self, screen, enSize):
        
        speedMod = 1

        if (self.lifetime > 0):
            self.lifetime -= (120/self.frameRate)*2
            self.deltaVal += (120/self.frameRate)*(speedMod)
        if (self.lifetime <= 0):
            self.deleteMe = True
        
        textRender = self.font.render("- " + str(format(self.value, '.2g')), True, self.color)
        textRect = textRender.get_rect(center = (self.posX + enSize/2, self.posY - self.deltaVal))
        screen.blit(textRender, textRect)