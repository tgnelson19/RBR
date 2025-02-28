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

        scalar = 2

        self.infoObject = pygame.display.Info() # Gets info about native monitor res
        self.sW, self.sH = (self.infoObject.current_w/scalar, self.infoObject.current_h/scalar)

        pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h))

        if scalar == 1:
            self.screen = pygame.display.set_mode([self.sW, self.sH], pygame.FULLSCREEN)  # Makes a screen that's that wide
        else:
            self.screen = pygame.display.set_mode([self.sW, self.sH])  # Makes a screen that's that wide

        self.clock = pygame.time.Clock()  # Main time keeper
        self.done = False  # Determines if the game is over or not

        self.fontSize = 30
        self.font = pygame.font.Font("media/coolveticarg.otf", self.fontSize)

        self.mouseDown = False
        self.mouseX, self.mouseY = 0,0

        self.keysDown = [False, False, False, False]

        self.character = Character(self.sW / 2, self.sH / 2)

        self.enemyWrangler = EnemyWrangler()

        self.background = Background(self.sW, self.sH)
        self.background.makeDefaultRoom()

        self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
        self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)

        

        self.baseNumKilledNeeded = 25
        self.baseOneInChance = 45
        self.numKilledNeeded = self.baseNumKilledNeeded
        self.oneInChance = self.baseOneInChance

        self.enemiesEnabled = True

        self.stage = 1



    def doTheTitleScreen(self):
        self.clock.tick(120)  # Keeps program to only 120 frames per second
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
        
        textRender = self.font.render("RbR : Press Space To Play", True, (0,0,0))
        textRect = textRender.get_rect(center = (self.sW/2, self.sH/2))
        self.screen.blit(textRender, textRect)

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_SPACE:
                    self.state = "gameRun"

        self.bugCheckerOnMousePos()
        self.finishPaint(pygame.Color(245,245,220))

    ##########################################################################################################

    def doAnUpdate(self): #Main Update Function

    ##########################################################################################################

        self.eventHandler()  # Updates with any potential user interaction (Don't Change)

    ##########################################################################################################

    # Put functions to do things here (Main chunks of code)

        self.background.displayCurrentRoom(self.screen)

        #self.bugCheckerOnMousePos() # Helps determine mouse position

        self.displayNumOfEnemiesKilled()

        playerDecision = self.character.moveAndDrawPlayer(self.screen, self.keysDown) # Moves player around the screen based on keysdown
        self.character.handlingBullets(self.screen, self.mouseDown, self.mouseX, self.mouseY)

        self.enemyWrangler.updateEnemies(self.screen, self.character.positionX, self.character.positionY)
        self.enemyWrangler.updateExperience(self.screen, self.background.tileSize, self.character.auraSpeed)
        self.enemyWrangler.hurtEnemies(self.character.liveRounds)
        
        self.enemyWrangler.expForPlayer(self.character.positionX, self.character.positionY, self.character.playerSize, self.character.aura)
        self.enemyWrangler.hurtPlayer(self.character.positionX, self.character.positionY, self.character.playerSize)

        self.enemyWrangler.expCount = self.character.shareExp(self.screen, self.enemyWrangler.expCount)

        if(self.enemyWrangler.dead == True):
            self.state = "titleScreen"


        if (self.enemyWrangler.numOfEnemiesKilled > self.numKilledNeeded):
            self.background.openDoors()
        elif(self.enemiesEnabled):
            self.enemyWrangler.makeANewEnemy("crawler", self.sW, self.sH, self.oneInChance)


        if (playerDecision != "no"):

            self.background.makeDefaultRoom()
            self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.numOfEnemiesKilled = 0
            self.numKilledNeeded += 5
            self.enemyWrangler.enemyList.clear()
            self.stage += 1
            self.enemyWrangler.experienceList.clear()

            if(self.oneInChance > 10):
                self.oneInChance -= 5
            elif(self.oneInChance > 5):
                self.oneInChance -= 2
            elif (self.oneInChance > 1):
                self.oneInChance -= 1
        
        if (playerDecision == "bottom"):
            self.character.positionX = (self.sW / 2) - (self.character.playerSize / 2)
            self.character.positionY = self.background.tileSize + 5
        elif (playerDecision == "left"):
            self.character.positionX = self.background.tileSize + 5
            self.character.positionY = (self.sH / 2) - (self.character.playerSize / 2)
        elif (playerDecision == "right"):
            self.character.positionX = self.sW - (self.background.tileSize + 5)
            self.character.positionY = (self.sH / 2) - (self.character.playerSize / 2)
        elif (playerDecision == "top"):
            self.character.positionX = (self.sW / 2) - (self.character.playerSize / 2)
            self.character.positionY = self.sH - (self.background.tileSize + 5)



    ##########################################################################################################

        self.finishPaint(pygame.Color(0,0,0))  # Paints whatever is desired from last frame on the screen (Don't Change)

    ##########################################################################################################
        
   
    def displayNumOfEnemiesKilled(self):
        textRender = self.font.render("Stage: " + str(self.stage), True, (0,0,0))
        textRect = textRender.get_rect(topleft = (35,35))
        self.screen.blit(textRender, textRect)
        textRender = self.font.render("Lv: " + str(self.character.currentLevel), True, (0,0,0))
        textRect = textRender.get_rect(topleft = (200,35))
        self.screen.blit(textRender, textRect)

    def bugCheckerOnMousePos(self):
        textRender = self.font.render(str(self.mouseX) + ", " + str(self.mouseY), True, (0,0,0))
        textRect = textRender.get_rect(topleft = (10,10))
        self.screen.blit(textRender, textRect)

    def finishPaint(self, color):
        pygame.display.flip()  # Displays currently drawn frame
        self.screen.fill(color)  # Clears screen with a black color

    def eventHandler(self):
        self.clock.tick(120)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True

                if event.key == pygame.K_w or event.key == pygame.K_UP: self.keysDown[0] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.keysDown[2] = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.keysDown[1] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.keysDown[3] = True

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
