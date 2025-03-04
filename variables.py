import pygame
from os import environ
from character import Character
from background import Background
from enemyWrangler import EnemyWrangler

class Variables:


    def __init__(self):

        self.state = "titleScreen"

        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()  # Initializes a window
        pygame.display.set_caption("Little Dude")

        scalar = 1 #For future use for non-fullscreen gameplay

        self.tileSizeGlobal = 40 #Global tile size that should hopefully not look too bad for people...
        
        self.frameRate = 120

        self.infoObject = pygame.display.Info() # Gets info about native monitor res
        self.sW, self.sH = (self.infoObject.current_w/scalar, self.infoObject.current_h/scalar)

        self.numTX = self.sW / self.tileSizeGlobal #Total number of X axis tiles
        self.numTY = self.sH / self.tileSizeGlobal #Total number of Y axis tiles

        pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h))

        if scalar == 1:
            self.screen = pygame.display.set_mode([self.sW, self.sH], pygame.FULLSCREEN)  # Makes a screen that's that wide
        else:
            self.screen = pygame.display.set_mode([self.sW, self.sH])  # Makes a screen that's that wide

        self.clock = pygame.time.Clock()  # Main time keeper
        self.done = False  # Determines if the game is over or not

        self.fontSize = int(self.tileSizeGlobal*(2/3))
        self.font = pygame.font.Font("media/coolveticarg.otf", self.fontSize)
        self.textColor = (245,245,220)

        self.mouseDown = False
        self.mouseX, self.mouseY = 0,0

        self.keysDown = [False, False, False, False]

        self.character = Character(self.sW / 2, self.sH / 2, self.tileSizeGlobal, self.numTX, self.numTY, self.sW, self.sH, self.frameRate)

        self.enemyWrangler = EnemyWrangler(self.tileSizeGlobal, self.frameRate)
        
        self.backgroundColor = pygame.Color(0,0,0)
        self.darkColor = pygame.Color(0,0,0)
        self.lightColor = pygame.Color(245,245,220)
        self.darkLightMode = "Dark"

        self.background = Background(self.sW, self.sH, self.tileSizeGlobal, self.backgroundColor)
        self.background.makeDefaultRoom()

        self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
        self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)

        self.highestLevel = 0

        self.baseNumKilledNeeded = 15
        self.baseOneInChance = 60
        self.numKilledNeeded = self.baseNumKilledNeeded
        self.oneInChance = self.baseOneInChance

        self.enemiesEnabled = True
        self.autoFire = False
        self.gracePeriodStart = self.frameRate*3
        self.gracePeriod = self.gracePeriodStart

        self.stage = 1
        
        



    def doTheTitleScreen(self):
        self.clock.tick(self.frameRate)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position

        self.enemyWrangler.enemyList.clear()
        self.enemyWrangler.experienceList.clear()
        self.enemyWrangler.numOfEnemiesKilled = 0
        self.character.positionX = self.sW / 2
        self.character.positionY = self.sH / 2
        self.background.makeDefaultRoom()
        self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
        self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)
        self.numKilledNeeded = self.baseNumKilledNeeded
        self.oneInChance = self.baseOneInChance
        self.stage = 1
        self.enemyWrangler.dead = False
        self.keysDown = [False, False, False, False]
        self.enemyWrangler.expCount = 0
        self.character.currentLevel = 0
        self.character.expNeededForNextLevel = self.character.baseExpNeededForNextLevel
        self.character.resetCharStats()
        self.enemyWrangler.stage = 1
        self.autoFire = False
        
        textRender = self.font.render("RbR : Press Space To Play", True, self.textColor)
        textRect = textRender.get_rect(center = (self.sW/2, self.sH/2))
        self.screen.blit(textRender, textRect)

        textRender = self.font.render("WASD to Move, Mouse to Shoot, I to Autofire, O for light/dark mode", True, self.textColor)
        textRect = textRender.get_rect(center = (self.sW/2, self.sH*(2/3)))
        self.screen.blit(textRender, textRect)

        textRender = self.font.render("Highest Level So Far: " + str(self.highestLevel), True, self.textColor)
        textRect = textRender.get_rect(center = (self.sW/2, self.sH*(4/5)))
        self.screen.blit(textRender, textRect)

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_SPACE:
                    self.state = "gameRun"
                if event.key == pygame.K_o:
                    if self.darkLightMode:
                        self.darkLightMode = False
                        self.backgroundColor = self.lightColor
                        self.textColor = self.darkColor
                    else:
                        self.darkLightMode = True
                        self.backgroundColor = self.darkColor
                        self.textColor = self.lightColor

        #self.bugCheckerOnMousePos()
        self.finishPaint(self.backgroundColor)

    ##########################################################################################################

    def doAnUpdate(self): #Main Update Function

    ##########################################################################################################

        self.eventHandler()  # Updates with any potential user interaction (Don't Change)

    ##########################################################################################################

    # Put functions to do things here (Main chunks of code)

        self.background.displayCurrentRoom(self.screen, self.backgroundColor)

        #self.bugCheckerOnMousePos() # Helps determine mouse position

        self.displayNumOfEnemiesKilled()

        
        if (self.autoFire):
            self.character.handlingBullets(self.screen, True, self.mouseX, self.mouseY)
        else:
            self.character.handlingBullets(self.screen, self.mouseDown, self.mouseX, self.mouseY)

        self.enemyWrangler.updateEnemies(self.screen, self.character.positionX, self.character.positionY)
        self.enemyWrangler.updateExperience(self.screen, self.background.tileSize, self.character.auraSpeed)
        self.enemyWrangler.hurtEnemies(self.character.liveRounds, self.character.damage)
        
        self.enemyWrangler.expForPlayer(self.character.positionX, self.character.positionY, self.character.playerSize, self.character.aura)
        newDamage = self.enemyWrangler.hurtPlayer(self.character.positionX, self.character.positionY, self.character.playerSize, self.character.defense)

        self.highestLevel = 0

        if (self.enemyWrangler.playerHit):
            self.character.healthPoints -= newDamage
            self.enemyWrangler.playerHit = False
            if (self.character.healthPoints <= 0):
                self.state = "titleScreen"
                self.highestLevel = self.character.currentLevel

        self.enemyWrangler.updateDamageTexts(self.screen, self.tileSizeGlobal)

        playerDecision = self.character.moveAndDrawPlayer(self.screen, self.keysDown) # Moves player around the screen based on keysdown

        self.enemyWrangler.expCount = self.character.shareExpAndHP(self.screen, self.enemyWrangler.expCount)
        
        if (self.enemyWrangler.numOfEnemiesKilled >= self.numKilledNeeded):
            self.background.openDoors()
        elif(self.enemiesEnabled and self.gracePeriod == 0):
            self.enemyWrangler.makeANewEnemy("crawler", self.sW, self.sH, self.oneInChance)
        else:
            self.gracePeriod -= 1

        if (playerDecision != "no"):

            self.gracePeriod = self.gracePeriodStart

            self.background.makeDefaultRoom()
            self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.numOfEnemiesKilled = 0
            self.numKilledNeeded += 5
            self.enemyWrangler.enemyList.clear()
            self.stage += 1
            self.enemyWrangler.stage = self.stage
            self.enemyWrangler.experienceList.clear()

            if(self.oneInChance > 10):
                self.oneInChance -= 5
            elif(self.oneInChance > 5):
                self.oneInChance -= 2
            elif (self.oneInChance > 1):
                self.oneInChance -= 1
        
            if (playerDecision == "bottom"):
                self.character.positionX = (self.sW / 2) - (self.background.tileSize / 2)
                self.character.positionY = self.background.tileSize + 5
            elif (playerDecision == "right"):
                self.character.positionX = self.background.tileSize + 5
                self.character.positionY = (self.sH / 2) - (self.background.tileSize/ 2)
            elif (playerDecision == "left"):
                self.character.positionX = self.sW - (self.background.tileSize*2 + 5)
                self.character.positionY = (self.sH / 2) - (self.background.tileSize / 2)
            elif (playerDecision == "top"):
                self.character.positionX = (self.sW / 2) - (self.background.tileSize / 2)
                self.character.positionY = self.sH - (self.background.tileSize*2 + 5)



    ##########################################################################################################

        self.finishPaint(pygame.Color(0,0,0))  # Paints whatever is desired from last frame on the screen (Don't Change)

    ##########################################################################################################
        
   
    def displayNumOfEnemiesKilled(self):
        textRender = self.font.render("Stage: " + str(self.stage), True, self.textColor)
        textRect = textRender.get_rect(topleft = (int(self.tileSizeGlobal*1.5), int(self.tileSizeGlobal/(25/3))))
        self.screen.blit(textRender, textRect)
        textRender = self.font.render("Level " + str(self.character.currentLevel), True, self.textColor)
        textRect = textRender.get_rect(topleft = (int(self.sW/1.65), int(self.tileSizeGlobal/(25/3))))
        self.screen.blit(textRender, textRect)
        textRender = self.font.render("Health ", True, self.textColor)
        textRect = textRender.get_rect(topleft = (int(self.sW/1.65), self.sH - self.tileSizeGlobal + int(self.tileSizeGlobal/(25/3))))
        self.screen.blit(textRender, textRect)
        if (self.numKilledNeeded - self.enemyWrangler.numOfEnemiesKilled > 0):
            textRender = self.font.render("Kills needed: " + str(self.numKilledNeeded - self.enemyWrangler.numOfEnemiesKilled), True, self.textColor)
            textRect = textRender.get_rect(center = (int(self.sW/2), int(self.tileSizeGlobal/(2))))
            self.screen.blit(textRender, textRect)
        

    def bugCheckerOnMousePos(self):
        textRender = self.font.render(str(self.mouseX) + ", " + str(self.mouseY), True, self.textColor)
        textRect = textRender.get_rect(topleft = (10,10))
        self.screen.blit(textRender, textRect)

    def finishPaint(self, color):
        pygame.display.flip()  # Displays currently drawn frame
        self.screen.fill(color)  # Clears screen with a black color

    def eventHandler(self):
        self.clock.tick(self.frameRate)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "titleScreen"

                if event.key == pygame.K_w or event.key == pygame.K_UP: self.keysDown[0] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.keysDown[2] = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.keysDown[1] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.keysDown[3] = True
                if event.key == pygame.K_i: 
                    if(self.autoFire == True):
                        self.autoFire = False
                    else:
                        self.autoFire = True
                if event.key == pygame.K_o:
                    if self.darkLightMode:
                        self.darkLightMode = False
                        self.backgroundColor = self.lightColor
                        self.textColor = self.darkColor
                    else:
                        self.darkLightMode = True
                        self.backgroundColor = self.darkColor
                        self.textColor = self.lightColor

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_UP: self.keysDown[0] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.keysDown[2] = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.keysDown[1] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.keysDown[3] = False
                    if event.key == pygame.K_BACKSPACE and self.enemiesEnabled == True: self.enemiesEnabled = False
                    elif event.key == pygame.K_BACKSPACE and self.enemiesEnabled == False: self.enemiesEnabled = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False
