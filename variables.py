import pygame
from os import environ
from character import Character
from background import Background
from enemyWrangler import EnemyWrangler
from levelingHandler import LevelingHandler

class Variables:


    def __init__(self):

        self.state = "titleScreen"

        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()  # Initializes a window
        pygame.display.set_caption("RotBoiRemastered")

        scalar = 1 #For future use for non-fullscreen gameplay

        self.tileSizeGlobal = 40 #Global tile size that should hopefully not look too bad for people...
        
        self.frameRate = 120 #Default maximum framerate for the game to run at

        self.infoObject = pygame.display.Info() # Gets info about native monitor res
        self.sW, self.sH = (self.infoObject.current_w/scalar, self.infoObject.current_h/scalar)

        self.numTX = self.sW / self.tileSizeGlobal #Total number of X axis tiles
        self.numTY = self.sH / self.tileSizeGlobal #Total number of Y axis tiles

        pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h))

        if scalar == 1:
            self.screen = pygame.display.set_mode([self.sW, self.sH], pygame.FULLSCREEN)  # Makes a screen that's fullscreen
        else:
            self.screen = pygame.display.set_mode([self.sW, self.sH])  # Makes a screen that's not fullscreen

        self.clock = pygame.time.Clock()  # Main time keeper
        self.done = False  # Determines if the game is over or not

        #Main font for the game to use for during-game display
        self.fontSize = int(self.tileSizeGlobal*(2/3))
        self.font = pygame.font.Font("media/coolveticarg.otf", self.fontSize)
        self.textColor = (245,245,220)

        #Variables to watch the mouse's actions
        self.mouseDown = False
        self.mouseX, self.mouseY = 0,0

        #List of W,A,S,D movement by the player
        self.keysDown = [False, False, False, False]

        #Initialize the character object that holds all of the core character statistics/updating/handling
        self.character = Character(self.sW / 2, self.sH / 2, self.tileSizeGlobal, self.numTX, self.numTY, self.sW, self.sH, self.frameRate)

        #Initialize the enemy wrangler, the device used to handle enemy/experience updating/handling
        self.enemyWrangler = EnemyWrangler(self.tileSizeGlobal, self.frameRate)
        
        #Light and dark mode colors
        self.backgroundColor = pygame.Color(0,0,0)
        self.darkColor = pygame.Color(0,0,0)
        self.lightColor = pygame.Color(245,245,220)
        self.darkLightMode = "Dark"

        #Initializing the background that is used for displaying the current tileset room the player is in
        self.background = Background(self.sW, self.sH, self.tileSizeGlobal, self.backgroundColor)
        self.background.makeDefaultRoom()
        self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize) #Generates zone player cannot move in
        self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize) #Generates zone experience orbs cannot move in

        #Initializing device used to handle character leveling up statistics
        self.levelingHandler = LevelingHandler(self.tileSizeGlobal, self.frameRate, pygame.Color(90,90,90), self.sW, self.sH)

        #Technically the current high score score-keeper
        self.highestLevel = 0

        #Basic variables necessary for handling the game's operation at the moment
        self.baseNumKilledNeeded = 15 #Base number of enemies needed to die to make it to next stage
        self.numKilledNeeded = self.baseNumKilledNeeded #Actual number of enemies needed to die for next stage
        self.baseOneInChance = 60 #Base one-in chance of an enemy spawning per frame
        self.oneInChance = self.baseOneInChance #Actual chance of an enemy spawning per frame
        self.gracePeriodStart = self.frameRate*3 #Grace period for enemies to spawn in new room / after leveling
        self.gracePeriod = self.gracePeriodStart #Grace period for enemies to spawn in new room / after leveling
        self.stage = 1 #Current stage level
        self.newRandoUps = False #Determines if upgrades have been randomized yet

        #Weird variables used for debugging / QOL
        self.enemiesEnabled = True
        self.autoFire = False
        
        
    #Completely cleans everything at title screen (Needs to be optimized for no wasted operations/resets)
    def doTheTitleScreen(self):
        self.clock.tick(self.frameRate)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position

        #Clears basic variables, resets playing field
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
        
        #Displays title texts on title screen
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
                    self.highestLevel = 0
                if event.key == pygame.K_o:
                    if self.darkLightMode:
                        self.darkLightMode = False
                        self.backgroundColor = self.lightColor
                        self.textColor = self.darkColor
                    else:
                        self.darkLightMode = True
                        self.backgroundColor = self.darkColor
                        self.textColor = self.lightColor

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False

        self.finishPaint(self.backgroundColor) #Paints to the screen






    ##########################################################################################################

    def doAnUpdate(self): #Main Update Function For Game

    ##########################################################################################################

        self.eventHandler()  # Updates with any potential user interaction (Don't Change)

    ##########################################################################################################

    # Put functions to do things here (Main chunks of code)

        self.background.displayCurrentDefaults(self.screen, self.backgroundColor) #Displays background tiles

        #Autofire logic
        if (self.autoFire):
            self.character.handlingBullets(self.screen, True, self.mouseX, self.mouseY)
        else:
            self.character.handlingBullets(self.screen, self.mouseDown, self.mouseX, self.mouseY)

        #Updates experience bubbles on screen first
        self.enemyWrangler.updateExperience(self.screen, self.background.tileSize, self.character.auraSpeed)

        #Updates leveling logic with respect to bubbles for player
        self.enemyWrangler.expForPlayer(self.character.positionX, self.character.positionY, self.character.playerSize, self.character.aura)

        #Determines if the player needs to be hurt on the current frame
        newDamage = self.enemyWrangler.hurtPlayer(self.character.positionX, self.character.positionY, self.character.playerSize, self.character.defense)

        if (self.enemyWrangler.playerHit):
            self.character.healthPoints -= newDamage
            self.enemyWrangler.playerHit = False
            if (self.character.healthPoints <= 0):
                self.state = "titleScreen"
                self.highestLevel = self.character.currentLevel

        #Update current damage texts that are still alive on the screen
        self.enemyWrangler.updateDamageTexts(self.screen)

        #Draws current enemies to the screen
        self.enemyWrangler.drawEnemies(self.screen)

        #Draws the walls of the background last to ensure enemies aren't on top of background
        self.background.displayCurrentWalls(self.screen, self.backgroundColor)

        #Draws the texts that are on top of the walls etc...
        self.displayMiscStats()

        #Moves and draws the player, determines if the player has entered a door and returns direction
        playerDecision = self.character.moveAndDrawPlayer(self.screen, self.keysDown) # Moves player around the screen based on keysdown

        #Determines how much exp the character has and if a level up is warrented
        tempExpHold = self.character.shareExpAndHP(self.screen, self.enemyWrangler.expCount)

        if (tempExpHold == "levelUp"):
            self.state = "leveling"
            self.enemyWrangler.expCount = 0
        else:
            self.enemyWrangler.expCount = tempExpHold

        #Grace period logic used to determine if enemies should spawn / be updated (i.e. after new room / level up)
        if (self.enemyWrangler.numOfEnemiesKilled >= self.numKilledNeeded):
            self.background.openDoors()
            if(self.gracePeriod <= 0):
                self.enemyWrangler.hurtEnemies(self.character.liveRounds, self.character.damage)
                self.enemyWrangler.updateEnemies(self.character.positionX, self.character.positionY)
        elif(self.enemiesEnabled and self.gracePeriod <= 0):
            self.enemyWrangler.updateEnemies(self.character.positionX, self.character.positionY)
            self.enemyWrangler.makeANewEnemy("crawler", self.sW, self.sH, self.oneInChance)
            self.enemyWrangler.hurtEnemies(self.character.liveRounds, self.character.damage)
        if(self.gracePeriod > 0):
            self.gracePeriod -= 1

        #When the player enters a new room...
        if (playerDecision != "no"):

            #Reset room-based statistics and prime for new room
            self.gracePeriod = self.gracePeriodStart
            self.character.healthPoints = self.character.maxHealthPoints
            self.background.makeDefaultRoom()
            self.character.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.newNoNoZone(self.background.currentLayout, self.background.tileSize)
            self.enemyWrangler.numOfEnemiesKilled = 0
            self.numKilledNeeded += 5
            self.enemyWrangler.enemyList.clear()
            self.stage += 1
            self.enemyWrangler.stage = self.stage
            self.enemyWrangler.experienceList.clear()

            #Make enemies spawn more frequently based off of crappy function
            if(self.oneInChance > 10):
                self.oneInChance -= 5
            elif(self.oneInChance > 5):
                self.oneInChance -= 2
            elif (self.oneInChance > 1):
                self.oneInChance -= 1
        
            #Spawn the player at the opposite door to provide a weird dungeon crawler aspect
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
        
   #Displays misc. statistics on top of the border
    def displayMiscStats(self):
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
            textRender = self.font.render("Kills Till Next Stage: " + str(self.numKilledNeeded - self.enemyWrangler.numOfEnemiesKilled), True, self.textColor)
            textRect = textRender.get_rect(center = (int(self.sW/2), int(self.tileSizeGlobal/(2))))
            self.screen.blit(textRender, textRect)
        
    #Displays the current mouseX and mouseY in the top left (debugging)
    def bugCheckerOnMousePos(self):
        textRender = self.font.render(str(self.mouseX) + ", " + str(self.mouseY), True, self.textColor)
        textRect = textRender.get_rect(topleft = (10,10))
        self.screen.blit(textRender, textRect)

    #Finishes a paint / draws the current frame to the screen
    def finishPaint(self, color):
        pygame.display.flip()  # Displays currently drawn frame
        self.screen.fill(color)  # Clears screen with a black color

    #Basic event handling...
    def eventHandler(self):
        self.clock.tick(self.frameRate)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program when windows x is clicked

            #For keys...
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "titleScreen"

                #Player movement
                if event.key == pygame.K_w or event.key == pygame.K_UP: self.keysDown[0] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.keysDown[2] = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.keysDown[1] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.keysDown[3] = True

                #Autofire
                if event.key == pygame.K_i: 
                    if(self.autoFire == True):
                        self.autoFire = False
                    else:
                        self.autoFire = True
                
                #Light/Dark Mode
                if event.key == pygame.K_o:
                    if self.darkLightMode:
                        self.darkLightMode = False
                        self.backgroundColor = self.lightColor
                        self.textColor = self.darkColor
                    else:
                        self.darkLightMode = True
                        self.backgroundColor = self.darkColor
                        self.textColor = self.lightColor

            #Ending player movement
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_UP: self.keysDown[0] = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN: self.keysDown[2] = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT: self.keysDown[1] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT: self.keysDown[3] = False
                    if event.key == pygame.K_BACKSPACE and self.enemiesEnabled == True: self.enemiesEnabled = False
                    elif event.key == pygame.K_BACKSPACE and self.enemiesEnabled == False: self.enemiesEnabled = True

            #Click logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False

    #Leveling logic, takes a bit to get used to and comments don't really help
    def LevelingLogic(self):

        self.clock.tick(self.frameRate)  # Keeps program to only 120 frames per second
        self.mouseX, self.mouseY = pygame.mouse.get_pos() # Saves current mouse position
        
        if (not self.newRandoUps):
            self.levelingHandler.randomizeLevelUp()
            self.keysDown = [False, False, False, False]
            self.newRandoUps = True

        for event in pygame.event.get():  # Main event handler
            if event.type == pygame.QUIT:
                self.done = True  # Close the entire program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "titleScreen"

            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseDown = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False

        self.levelingHandler.drawCards(self.screen)
        pDecision = self.levelingHandler.PlayerClicked(self.mouseDown, self.mouseX, self.mouseY)

        if (pDecision == "leftCard"):
            if (self.levelingHandler.leftCardUpgradeMath == "addative"):
                self.character.collectiveAddStats[self.levelingHandler.leftCardUpgradeType].append(self.levelingHandler.upgradeRarity[self.levelingHandler.leftCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesAdd[self.levelingHandler.leftCardUpgradeType])
            if (self.levelingHandler.leftCardUpgradeMath == "multiplicative"):
                self.character.collectiveMultStats[self.levelingHandler.leftCardUpgradeType].append(1 + self.levelingHandler.upgradeRarity[self.levelingHandler.leftCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesMult[self.levelingHandler.leftCardUpgradeType])

        elif (pDecision == "midCard"):
            if (self.levelingHandler.midCardUpgradeMath == "addative"):
                self.character.collectiveAddStats[self.levelingHandler.midCardUpgradeType].append(self.levelingHandler.upgradeRarity[self.levelingHandler.midCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesAdd[self.levelingHandler.midCardUpgradeType])
            if (self.levelingHandler.midCardUpgradeMath == "multiplicative"):
                self.character.collectiveMultStats[self.levelingHandler.midCardUpgradeType].append(1 + self.levelingHandler.upgradeRarity[self.levelingHandler.midCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesMult[self.levelingHandler.midCardUpgradeType])

        elif (pDecision == "rightCard"):
            if (self.levelingHandler.rightCardUpgradeMath == "addative"):
                self.character.collectiveAddStats[self.levelingHandler.rightCardUpgradeType].append(self.levelingHandler.upgradeRarity[self.levelingHandler.rightCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesAdd[self.levelingHandler.rightCardUpgradeType])
            if (self.levelingHandler.rightCardUpgradeMath == "multiplicative"):
                self.character.collectiveMultStats[self.levelingHandler.rightCardUpgradeType].append(1 + self.levelingHandler.upgradeRarity[self.levelingHandler.rightCardUpgradeRarity] * self.levelingHandler.upgradeBasicTypesMult[self.levelingHandler.rightCardUpgradeType])

        if (pDecision != "none"):
            self.character.combarinoPlayerStats()
            self.newRandoUps = False
            self.gracePeriod = self.frameRate * 2
            self.state = "gameRun"


        pygame.display.flip()  # Displays currently drawn frame