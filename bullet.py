import pygame
from math import sin, cos, sqrt, degrees

#Handles basic bullet statistics used during game calculation
class Bullet:

    def __init__(self, pX, pY, speed, direc, bRange, size, color, pierce, damage, currCrit, sW, sH, frameRate):
        self.posX = pX
        self.posY = pY
        self.iPosX = pX
        self.iPosY = pY
        self.sW = sW
        self.sH = sH
        self.speed = speed
        self.direc = direc
        self.size = size
        self.color = color
        self.bRange = bRange
        self.bPierce = pierce
        self.remFlag = False
        self.frameRate = frameRate
        self.damage = damage
        self.currCrit = currCrit


        # 1) Load your custom image
        #    Make sure "my_bullet.png" is in the correct folder (or provide a full path).
        #    convert_alpha() helps maintain transparency if the image has an alpha channel.
        self.bullet_image = pygame.image.load("assets/projectile-png.png").convert_alpha()

        # 2) Optionally, scale it to match your bullet size if needed
        #    e.g. transform.scale to (width, height). If your bullet is square, do (size, size):
        self.bullet_image = pygame.transform.scale(self.bullet_image, (int(self.size), int(self.size)))

    def updateAndDrawBullet(self, screen):

        self.posX = self.posX + (self.speed*cos(self.direc)) * (120/self.frameRate)
        self.posY = self.posY - (self.speed*sin(self.direc)) * (120/self.frameRate)

        if(self.posX >= self.sW):
            self.posX = self.sW - 1
            self.remFlag = True
        elif(self.posX <= 0):
            self.posX = 1
            self.remFlag = True
        if(self.posY >= self.sH):
            self.posY = self.sH-1
            self.remFlag = True
        elif(self.posY <= 0):
            self.posY = 1
            self.remFlag = True

        #pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.size, self.size))

        angle_deg = degrees(self.direc)  # or with some + offset
        rotated_image = pygame.transform.rotate(self.bullet_image, angle_deg)

        # Create a rect so the center is at (posX, posY)
        rotated_rect = rotated_image.get_rect(center=(self.posX+self.size/2, self.posY +self.size/2))

        # Now blit so the bullet’s center remains at self.posX, self.posY
        screen.blit(rotated_image, rotated_rect)


        #if(sqrt((abs(self.posX - self.iPosX) ** 2) + (abs(self.posY - self.iPosY) ** 2)) >= self.bRange): 
        
        # 2) Check bullet travel distance
        dist_traveled = sqrt((self.posX - self.iPosX) ** 2 + (self.posY - self.iPosY) ** 2)
        if dist_traveled >= self.bRange:
            self.remFlag = True