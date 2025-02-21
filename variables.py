import pygame
from os import environ
from character import Character

class Variables:


    def __init__(self):

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



    ##########################################################################################################

    def doAnUpdate(self): #Main Update Function

    ##########################################################################################################

        self.eventHandler()  # Updates with any potential user interaction (Don't Change)

    ##########################################################################################################

    # Put functions to do things here (Main chunks of code)

        self.bugCheckerOnMousePos() # Helps determine mouse position

        self.character.movePlayer(self.screen, self.keysDown) # Moves player around the screen based on keysdown





    ##########################################################################################################

        self.finishPaint()  # Paints whatever is desired from last frame on the screen (Don't Change)

    ##########################################################################################################
        
   


    def bugCheckerOnMousePos(self):
        textRender = self.font.render(str(self.mouseX) + ", " + str(self.mouseY), True, (255,255,255))
        textRect = textRender.get_rect(topleft = (10,10))
        self.screen.blit(textRender, textRect)

    def finishPaint(self):
        pygame.display.flip()  # Displays currently drawn frame
        self.screen.fill(pygame.Color(0, 0, 0))  # Clears screen with a black color

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False
