from variables import Variables

vars = Variables()  # Variable Holster Object

while not vars.done:  # Loop to render each frame

    #This state is the title screen
    if vars.state == "titleScreen":
        vars.doTheTitleScreen()

    #This state is when the player reaches a level up
    elif vars.state == "leveling":
        vars.LevelingLogic()

    #This state is when the game runs
    elif vars.state == "gameRun": 
        vars.doAnUpdate()  

    