import pygame, time, random, sys
from classes import *
from num2words import num2words
global playerColor, endTime, firstFrame
global mazes, mazeLevel, allMazes, mazeCoordinates, customMaze, usePreset, r, g, b

r = 0             #custom RGB maze color (red value)
g = 0             #custom RGB maze color (green value)
b = 0             #custom RGB maze color (blue value)
usePreset = True  #set use preset colors as true
customMaze = (r, g, b)  #set custom maze to black as default
mazeLevel = 1     #the default maze
squareSize = 25   #size (in px) of each square in the maze    
playerColors = ['Red', 'Black', 'White', 'Blue', 'Green', 'Yellow']     #list of all the colors the player can be
playerColor = 0   #index of the current player color
endTime = 0       #time survived/time it took to win
firstFrame = True #first frame of menu scene

def game():
    global endTime #endTime is global, so it is accessible by 'win()' and 'lose()' functions
    '''
      The game scene.
      
      This scene is where the player actually plays the game.

    '''
    
    #The code inbetween the lines is the initilization of the game:
    #--------------------------------------------------------------------
    pygame.init()                #prepare the pygame module for use
    surfaceSize = 480   
    
    clock = pygame.time.Clock()  #Force frame rate to be slower
    frameRate = 10

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    #load the font
    font = pygame.font.Font('CrazytoonDemoRegular.ttf', 10)
    
    #load and play the music
    pygame.mixer.music.load('For_Your_Life.mp3')
    pygame.mixer.music.play(-1)     #loop the music
    
    if mazeColor == 0:
        #maze is black...?
        enemyColor = 'Stealth'    #...set enemies to stealth color
    else:
        enemyColor = 'Rainbow'    #...set enemies to rainbow color
        
    scale = 0.5     #the scale of the player and enemy sprites
    
    #initialize the player:
    p1 = Player(mainSurface, [9, 9], scale, [0, 0, scale*48, scale*48], playerColors[playerColor], squareSize, mazeLevel)
    
    #initialize the turrets:
    turrets=[]     #variable where the turrets are stored
    if mazeLevel == 1:
        #Class(surface, coordinates, random delay between shots, square size, facing direciton)
        turrets.append(Turret(mainSurface, [2, 2], random.randint(25, 55), squareSize, 'right'))
        turrets.append(Turret(mainSurface, [13, 7], random.randint(25, 55), squareSize, 'left'))
        turrets[1].flip()    #flip the second turret so that it faces the right direction
    elif mazeLevel == 2:
        turrets.append(Turret(mainSurface, [3, 5], random.randint(20, 45), squareSize, 'right'))
        turrets.append(Turret(mainSurface, [12, 2], random.randint(20, 45), squareSize, 'left'))
        turrets[1].flip()
    elif mazeLevel == 3:
        turrets.append(Turret(mainSurface, [4, 5], random.randint(15, 30), squareSize, 'right'))
        turrets.append(Turret(mainSurface, [9, 2], random.randint(15, 30), squareSize, 'left'))
        turrets[1].flip()
    
    #initialize the enemies into the list 'enemies':
    enemies=[]
    for i in range(0, 3):
        enemies.append(Enemy(mainSurface, scale, [0, 0, scale*48, scale*48], enemyColor, squareSize, mazeLevel))
    eCounter = 0    #variable that increases until a certain value. When value is reached, the enemies move.
    
    #initialize the coins into the list 'coins':
    coins=[]
    for i in range(0, 20):
        coins.append(Coin(mainSurface, scale/5, squareSize, mazeLevel))
    
    #get the time to be used when calculting time survied
    timeStart = time.time()
    #--------------------------------------------------------------------
    
    # The main loop:
    while True:
        #check if ALL the coins are collected
        collected = False     #assume that they are NOT all collected
        for i in coins:
            #loop through all coins
            if i.collected == True:
                #current coin collected...?
                collected = True
            else:
                #if even one coin is not collected, break out of the loop
                collected = False
                break
        if collected:
            #player is alive and all coins are collected...?
            pygame.mixer.music.stop()       #...stop the music
            pygame.mixer.music.unload()     #...unload the music
            endTime = round(time.time() - timeStart, 2)      #...calculate, and round, the end time
            del p1    #...delete the player object
            win()     #...start the win scene

        ev = pygame.event.poll()    #look for any event
        if ev.type == pygame.QUIT:  #window close button clicked...?
            pygame.quit()     #...close pygame
            sys.exit()        #...stop the program
        if ev.type == pygame.KEYDOWN:   #key pressed down...?   
            p1.movePlayer(ev.key)     #...start the movePlayer function
        if ev.type == pygame.MOUSEBUTTONDOWN:   #mouse button pressed down...?
            x, y = pygame.mouse.get_pos()     #...get the position of the mouse
            if x >= 0 and x <= squareSize*2 and y >= 0 and y <= squareSize:
                #mouse position is inside of the '(back to) menu' button...?
                pygame.mixer.music.stop()     #...stop the music
                pygame.mixer.music.unload()   #...unload the music
                del p1                        #...delete the player object
                menu()                        #...start the menu scene
            
        for i in range(0, len(coins)):
            #loop through the coins
            if coins[i].coinCoordinates == p1.playerCoordinates:
                #player is at the same position of the current coin...?
                coins[i].collected = True     #...set current coin to collected

        mainSurface.fill(black)     #draw background
        
        if usePreset:
            #using preset maze colors...?
            drawMaze(mainSurface, squareSize, mazeColors[mazeColor])    #...draw the maze
        else:
            #using custom RGB maze color...?
            drawMaze(mainSurface, squareSize, customMaze)     #...draw the maze  
        
        #Draw the main menu button:
        pygame.draw.rect(mainSurface, red, (0, 0, squareSize * 2, squareSize))      #draw the button background
        text = 'Main'     #set first text variable
        text2 = 'Menu'    #set second text variable
        renderedText = font.render(text, 1, black)     #render the first text
        renderedText2 = font.render(text2, 1, black)   #render the second text
        mainSurface.blit(renderedText, (squareSize/2 - 3, 0))     #draw the first text
        mainSurface.blit(renderedText2, (squareSize/2 - 3, 11))   #draw the second text

        if eCounter == 10:
            #eCounter is 10...?
            for i in range(0, len(enemies)):
                #...loop through enemies
                enemies[i].moveEnemy(p1.playerCoordinates)    #...move the enemies
            eCounter = 0     #...reset eCounter
        
        p1.drawPlayer()     #draw the player
        
        for i in range(0, len(turrets)):
            #loop through the turrets
            turrets[i].draw()     #display the current turret
            
            if turrets[i].shotCounter == turrets[i].shotDelayLength and turrets[i].shooting == False:
                #current turret is ready to shoot and isn't currently shooting
                turrets[i].shooting = True      #...set the current turret to shooting
                if turrets[i].direction == 'right':
                    #...current turret is facing right...?
                    turrets[i].laserPos=[turrets[i].pos[0] + 37, turrets[i].pos[1] + 5]    #...set the laser position
                else:
                    #...current turret is facing left...?
                    turrets[i].laserPos=[turrets[i].pos[0] - 37, turrets[i].pos[1] + 5]    #...set the laser position
        
        for i in range(0, len(turrets)):
            #loop through turrets
            if turrets[i].shooting == True:
                #current turret is shooting...?
                if turrets[i].shoot(p1.playerPos) == None:
                    #...current turrets laser isn't touching the player
                    turrets[i].shoot(p1.playerPos)     #display the current turrets laser
                else:
                    #...current turrets laser hit the player...?
                    pygame.mixer.music.stop()     #...stop the music
                    pygame.mixer.music.unload()   #...unload the music
                    endTime = round(time.time() - timeStart, 2)   #...calculate the end time
                    del p1                        #...delete the player object
                    lose()                        #...start the lose scene
            
        for i in range(0, len(coins)):
            #loop through the coins
            if coins[i].collected == False:
                #if current coin isn't collected...
                coins[i].drawCoin()     #...draw the coin
        
        for i in range(0, len(enemies)):
            #loop through the enemies
            enemies[i].drawEnemy()     #draw the current enemy
        
        #check for player/enemy collision
        for i in range(0, len(enemies)):
            #loop through the enemies
            if enemies[i].enemyCoordinates == p1.playerCoordinates:
                #current enemy coordinates are the same as the players'...?
                pygame.mixer.music.stop()     #...stop the music
                pygame.mixer.music.unload()   #...unload the music
                endTime = round(time.time() - timeStart, 2)   #...calculate the end time
                del p1                        #...delete the player object
                lose()                        #...start the lose scene
               
        #check for enemies on the same spot:
        same = False     #assume that the enemies are not on the same spot       
        li=[]            #store enemy coordinates in this list 
        for i in range(0, len(enemies)):
            #loop through enemies
            #add the enemy coordinates to the list
            li.append(str(f'{enemies[i].enemyCoordinates[0]}{enemies[i].enemyCoordinates[1]}'))
        se = set(li)     #remove all duplicates from the list
        
        if len(li) != len(se):
            #length of the list is not the same as the set...?
            same = True     #...enemies on the same spot
                
        if same == True:
            #enemies on the same spot...?
            for i in range(0, len(enemies)):
                #...loop through the enemies
                while True:
                    #give the current enemy a new random coordinate until requirements are met
                    enemies[i].enemyCoordinates = [(random.randint(1, 16)), (random.randint(1, 8))]
                    if enemies[i].enemyCoordinates not in mazeCoordinates and enemies[i].enemyCoordinates != p1.playerCoordinates:
                        #new enemy coordinate is not in maze coordinates or equal to player coordinates...?
                        break   #...break out of loop
                enemies[i].updateEnemy()    #...update the enemy position
                
        eCounter += 1    #update eCounter (used to delay enemy movement)
        
        pygame.display.flip()    #display the surface
        
        clock.tick(frameRate)    #force the frame rate to be slower
#-------------------------------------

def menu():
    '''
    The main menu scene.
    '''  
    global mazeCoordinates, firstFrame
    
    #The code inbetween the lines is the initilization of the game:
    #--------------------------------------------------------------------
    pygame.init()      #prepare the pygame module for use
    surfaceSize = 480
    
    clock = pygame.time.Clock()  #force frame rate to be slower
    frameRate = 60

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    if firstFrame:
        #first frame of the menu scene...?
        mazeOutline()       #...add the outline of the maze to maze coordinates
        firstFrame = False  #...no longer the first frame
    
    #Load fonts
    font = pygame.font.Font('CrazytoonDemoRegular.ttf', 55)
    font2 = pygame.font.Font('CrazytoonDemoRegular.ttf', 35)
    
    #Load the and play the music
    pygame.mixer.music.load('For_Your_Life.mp3')
    pygame.mixer.music.play(-1)     #loop the music
    
    #menu sprites colors:
    col=['Black', 'Blue', 'Green', 'White', 'Yellow', 'Red', 'Stealth']
    
    sprites=[]    #create variable to store the menu sprites
    
    for i in range(1, 8):
        #loop through range one to eight
        if i == 1 or i == 2:
            #first or second loop through...?
            #...create the menu sprites and set them to alive
            sprites.append(MenuSprite(mainSurface, [(-60 * i), 400], True, random.randint(4, 6), col[i-1])) 
        else:
            #...create the menu sprites and set them to not alive
            #...spread them out differently based on current loop through
            if i < 5:
                sprites.append(MenuSprite(mainSurface, [(-60 * i) + 100, 400], False, random.randint(4, 6), col[i-1])) 
            else:
                sprites.append(MenuSprite(mainSurface, [(-60 * i) + 175, 400], False, random.randint(4, 6), col[i-1])) 

    index = 0        #current menu sprite being focused on
    victLap = False  #additional animation not being executed yet
    #--------------------------------------------------------------------
    while True:
        ev = pygame.event.poll()     #check for any events
        if ev.type == pygame.QUIT:   #close window button is pressed...?
            pygame.quit()     #...close pygame
            sys.exit()        #...stop the program
        if ev.type == pygame.MOUSEBUTTONDOWN:   #mouse button is pressed...?
            mouseX, mouseY = pygame.mouse.get_pos()    #...get the mouse position
            if mouseX >= 51 and mouseX <= 144 and mouseY >= 133 and mouseY < 167:
                #mouse position inside game button...?
                pygame.mixer.music.stop()     #...stop the music
                pygame.mixer.music.unload()   #...unload the music
                game()                        #...start game scene
            elif mouseX >= 249 and mouseX <= 428 and mouseY >= 132 and mouseY <= 165:
                #mouse position inside settings button...?
                settings()    #...start the settings scene
            elif mouseX >= 45 and mouseX <= 147 and mouseY >= 232 and mouseY <= 271:
                #mouse position inside help button...?
                pHelp()     #...start the help scene
            print(mouseX, mouseY)     #print the mouse position
            
        mainSurface.fill(black)     #set the background to black
        
        #Draw the game name:
        text = 'LASER MAZE'     #set the text variable
        renderedText = font.render(text, 1, red)     #render the text
        mainSurface.blit(renderedText, (50, 35))     #draw the text

        #Draw the play button:
        text = 'PLAY'     #set the text variable
        renderedText = font2.render(text, 1, blue)     #render the text
        mainSurface.blit(renderedText, (50, 135))      #draw the text
        
        #Draw the setting button:
        text = 'SETTINGS'     #set the text variable
        renderedText = font2.render(text, 1, yellow)     #render the text
        mainSurface.blit(renderedText, (250, 135))       #draw the text
        
        #Draw the help button:
        text = 'HELP'     #set the text variable
        renderedText = font2.render(text, 1, green)     #render the text
        mainSurface.blit(renderedText, (50, 235))       #draw the text
        
        for i in sprites:
            #loop through the menu sprites
            i.draw()     #draw the current sprite
         
        if victLap:
            #victory lap is true...?
            if sprites[6].pos[0] < 500:
                #...if sprite[6]'s x-pos is less than 500...?
                i.draw()     #...draw the current sprite (sprite[6])
            else:
                victLap = False     #...victory lap is finished
                index = 0           #...reset the index
                for i in range(0, len(sprites)):
                    #...loop through menu sprites
                    del sprites[0]     #...delete the first sprite
                for i in range(1, 8):
                    #...loop through range 1 to 8
                    if i == 1 or i == 2:
                        #...first or second loop through...?
                        #...create the menu sprites and set them to alive
                        sprites.append(MenuSprite(mainSurface, [(-60 * i), 400], True, random.randint(4, 6), col[i-1])) 
                    else:
                        #...create the menu sprites and set them to not alive
                        #...spread them out differently based on current loop through
                        if i < 5:
                            sprites.append(MenuSprite(mainSurface, [(-60 * i) + 100, 400], False, random.randint(4, 6), col[i-1])) 
                        else:
                            sprites.append(MenuSprite(mainSurface, [(-60 * i) + 175, 400], False, random.randint(4, 6), col[i-1])) 

        else:
            #the main animation:
            if sprites[index+1].shotDelay == 200 and sprites[index+1].doneShot == False:
                #second sprite has not shot, and is ready to...?
                bullet = Bullet(mainSurface, sprites[index+1].pos, sprites[index].pos)    #...initalialize the bullet
                sprites[index+1].shotDelay = 0    #...reset shot delay
                sprites[index+1].shot = True      #...set shot to true
            if sprites[index+1].shot == True:
                #shot is true...?
                if bullet.draw() == True:
                    #...bullet draw has returned that it hit a sprite...?
                    if index != 5:
                        #...is not the 5th menu sprite...?
                        sprites[index].alive = False     #...set that sprite to not alive   
                        sprites[index+1].shot = False    #...set the next sprite shot to false
                        sprites[index+1].doneShot = True #...set the next sprite done shot to true
                        del bullet                       #...delete the bullet object
                        sprites[index+2].alive = True    #...set the next, next sprite to alive
                        index += 1                       #...increase index by one
                    elif index == 5:
                        #...is the 5th menu sprite...?
                        sprites[index].alive = False     #...set that sprite to not alive
                        sprites[index+1].shot = False    #...set the next sprite shot to false
                        sprites[index+1].doneShot = True #...set the sprite done shot to true
                        del bullet                       #...delete the bullet object
                        victLap = True                   #...set the victory lap to true
                else:
                    #...draw the bullet
                    bullet.draw()

        pygame.display.flip()     #display the surface
        
        clock.tick(frameRate)     #force the frame rate to be slower
#---------------------------------

def settings():
    '''
    The settings scene.
    '''
    global playerColor, mazeColor, mazeLevel, mazeCoordinates, customMaze, usePreset, r, g, b
    pygame.init()      #prepare the pygame module for use
    surfaceSize = 480
    
    clock = pygame.time.Clock()  #force frame rate to be slower
    frameRate = 60

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    #load fonts:
    font = pygame.font.Font('CrazytoonDemoRegular.ttf', 26)
    font2 = pygame.font.SysFont('Arial', 26)
        
    while True:  
        ev = pygame.event.poll()    #look for any event
        if ev.type == pygame.QUIT:  #window close button clicked...?
            pygame.quit()     #...close pygame
            sys.exit()        #...stop the program 
        if ev.type == pygame.MOUSEBUTTONDOWN:    #mouse button pressed down...?
            mouseX, mouseY = pygame.mouse.get_pos()    #...get the mouse position
            if mouseX >= 0 and mouseX <= 100 and mouseY >= 440 and mouseY <= 480:
                #mouse position inside back to menu button...?
                menu()     #...start the menu scene
            elif mouseX >= 50 and mouseX <= 366 and mouseY >= 99 and mouseY <= 126:
                #mouse position inside player color button...?
                if playerColor < len(playerColors)-1:
                    #...player color is not the last color...?
                    playerColor += 1    #...add one to the player color
                else:
                    playerColor = 0     #...reset the player color to 0
            elif mouseX >= 50 and mouseX <= 223 and mouseY >= 200 and mouseY <= 226:
               if usePreset == False:
                   usePreset = True
                   #reset cutom rgb color:
                   r = 0
                   g = 0
                   b = 0
               #mouse position inside maze color button...?
               if mazeColor == len(mazeColors)-1:
                    #...maze color is the last color...?
                    mazeColor = 0     #...reset the maze color to 0
               else:
                    mazeColor += 1    #...add one to the player color
            elif mouseX >= 50 and mouseX <= 352 and mouseY >= 300 and mouseY <= 326:
                #mouse position inside maze level button...?
                if mazes != 1:
                    #...mulitple mazes avalible for use...?
                    if mazeLevel == mazes:
                        #...maze level is the last avalible maze...?
                        mazeLevel = 1    #...reset the maze level to one
                    else:
                        mazeLevel += 1   #...add one to the maze level
                    mazeCoordinates = allMazes[mazeLevel - 1]    #set maze coordinates to the current maze in selection
                    mazeOutline()     #add the outline to the maze coordinates
            elif mouseX >= 281 and mouseX <= 358 and mouseY >= 161 and mouseY <= 184:
                if usePreset:
                    usePreset = False
                if r <= 250:
                    r += 5
                else:
                    r = 0
                customMaze = (r, g, b)
            elif mouseX >= 271 and mouseX <= 369 and mouseY >= 190 and mouseY <= 215:
                if usePreset:
                    usePreset = False
                if g <= 250:
                    g += 5
                else:
                    g = 0
                customMaze = (r, g, b)
            elif mouseX >= 281 and mouseX <= 359 and mouseY >= 222 and mouseY <= 241:
                if usePreset:
                    usePreset = False
                if b <= 250:
                    b += 5
                else:
                    b = 0
                customMaze = (r, g, b)
            print(mouseX, mouseY)     #print the mouse position
            
        #draw the background
        mainSurface.fill(black)
        
        pygame.draw.rect(mainSurface, red, [0, 440, 100, 480])    #back to main menu button background
        text = 'BACK'    #set the text
        renderedText = font.render(text, 1, black)    #render the text
        mainSurface.blit(renderedText, (13, 447))     #display the text
             
        #RGB maze color selector:
        #load the texts:
        text = f'Red: {str(r)}'
        text2 = f'Green: {str(g)}'
        text3 = f'Blue: {str(b)}'
        #render the texts:
        renderedText = font2.render(text, 1, red)
        renderedText2 = font2.render(text2, 1, green)
        renderedText3 = font2.render(text3, 1, blue)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(320, 175))
        text_rect2 = renderedText2.get_rect(center=(320, 205))
        text_rect3 = renderedText3.get_rect(center=(320, 235))
        #display the text:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        mainSurface.blit(renderedText3, text_rect3)

        text = f'Player Color     {playerColors[playerColor]}'     #set the text
        renderedText = font.render(text, 1, pink)     #render the text
        mainSurface.blit(renderedText, (50, 100))     #display the text
        
        if mazeColor == 0:
            #maze color is black...?
            pygame.draw.rect(mainSurface, white, [45, 193, 190, 42])    #... display maze color button background as white
        
        text = f'Maze Color'     #set the text
        if usePreset:
            renderedText = font.render(text, 1, mazeColors[mazeColor])     #render the text
        else:
            renderedText = font.render(text, 1, (r, g, b))     #render the text
        mainSurface.blit(renderedText, (50, 200))              #display the text
        
        #maze option button
        text = f'Maze level     {num2words(mazeLevel)}'    #set the text
        renderedText = font.render(text, 1, red)           #render the text
        mainSurface.blit(renderedText, (50, 300))          #display the text
        
        pygame.display.flip() #display the surface
        
        clock.tick(frameRate) #force frame rate to be slower
#-----------------

def pHelp():
    '''
    The help scene.
    '''
    pygame.init()      #prepare the pygame module for use
    surfaceSize = 480 
    
    clock = pygame.time.Clock()  #force the frame rate to be slower

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    #load fonts
    font = pygame.font.SysFont('Arial', 12)
    font2 = pygame.font.SysFont('Arial', 30)
    font3 = pygame.font.SysFont('Arial', 26)

    #load and transform image of player
    player = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/CHARACTER_SPRITES/Red/Gunner_Red_Run.png')
    player = pygame.transform.smoothscale(player, (1.5*player.get_width(),1.5*player.get_height()))

    #load and transform image of coin
    coin = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/Spinning_Coin.png')
    coin = pygame.transform.smoothscale(coin, (0.5*coin.get_width(), 0.5*coin.get_height()))

    #load and transform image of turret
    turret = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/Turret.png')
    turret = pygame.transform.smoothscale(turret, (3*turret.get_width(), 3*turret.get_height()))

    #load and transform image of enemy
    enemy = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/CHARACTER_SPRITES/Rainbow/Gunner_Rainbow_Idle.png')
    enemy = pygame.transform.smoothscale(enemy, (1.5*enemy.get_width(),1.5*enemy.get_height()))

    while True:
        ev = pygame.event.poll()    #look for any events 
        if ev.type == pygame.MOUSEBUTTONDOWN:     #mouse button pressed down...?
            mouseX, mouseY = pygame.mouse.get_pos()     #...get the mouse position
            if mouseX >= 0 and mouseX <= 100 and mouseY >= 440 and mouseY <= 480:
                #mouse position is inside bak to menu button...?
                menu()    #...start the menu scene
            print(mouseX, mouseY)     #print the mouse position       
        
        mainSurface.fill(black)     #draw the background
    
        pygame.draw.rect(mainSurface, red, [0, 440, 100, 480])     #draw main menu button background
        text = 'BACK'     #set the text
        renderedText = font3.render(text, 1, black)    #render the text
        mainSurface.blit(renderedText, (13, 447))      #display the text
        
        #Player help:
        text = 'Player:'     #set the text
        renderedText = font2.render(text, 1, green)         #render the text
        text_rect = renderedText.get_rect(center=(75, 20))  #set text align to center
        mainSurface.blit(renderedText, text_rect)           #display the text
        #set the texts:
        text = 'Use WASD to move. You can'   
        text2 = 'change the player color'     
        text3 = 'in settings.'
        #render the texts:
        renderedText = font.render(text, 1, green)   
        renderedText2 = font.render(text2, 1, green)  
        renderedText3 = font.render(text3, 1, green)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(75, 45))
        text_rect2 = renderedText2.get_rect(center=(75, 60))
        text_rect3 = renderedText3.get_rect(center=(75, 75))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        mainSurface.blit(renderedText3, text_rect3)
        #display the player image:
        mainSurface.blit(player, (35, 90), [0, 0, (288/6)*1.5, 48*1.5])

        #Coin help:
        text = 'Coins:'     #set the text
        renderedText = font2.render(text, 1, yellow)         #render the text
        text_rect = renderedText.get_rect(center=(230, 20))  #set text align to center
        mainSurface.blit(renderedText, text_rect)            #display the text
        #set the texts:
        text = 'Coins are collected by'
        text2 = 'moving through them.'
        #render the texts:
        renderedText = font.render(text, 1, yellow)
        renderedText2 = font.render(text2, 1, yellow)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(230, 45))
        text_rect2 = renderedText2.get_rect(center=(230, 60))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        #display the coin image
        mainSurface.blit(coin, (200, 55), [0, 0, (700/6)*0.5, 200*0.5])

        #Enemy help:
        text = 'Enemy:'     #set the text
        renderedText = font2.render(text, 1, red)              #render the text
        text_rect = renderedText.get_rect(center=(380, 310))   #set the text align to center
        mainSurface.blit(renderedText, text_rect)              #display the text
        #set the texts:
        text = 'Enemies will move towards you. If'
        text2 = 'they touch you, you lose. If 2, or'
        text3 = 'more enemies occupy the same'
        text4 = 'spot, all enemies will teleport to a'
        text5 = 'new random spot.'
        #render the texts:
        renderedText = font.render(text, 1, red)
        renderedText2 = font.render(text2, 1, red)
        renderedText3 = font.render(text3, 1, red)
        renderedText4 = font.render(text4, 1, red)
        renderedText5 = font.render(text5, 1, red)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(380, 345))
        text_rect2 = renderedText2.get_rect(center=(380, 360))
        text_rect3 = renderedText3.get_rect(center=(380, 375))
        text_rect4 = renderedText4.get_rect(center=(380, 390))
        text_rect5 = renderedText5.get_rect(center=(380, 405))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        mainSurface.blit(renderedText3, text_rect3)
        mainSurface.blit(renderedText4, text_rect4)
        mainSurface.blit(renderedText5, text_rect5)
        #display the enemy image:
        mainSurface.blit(enemy, (345, 420), [0, 0, (288/6)*1.5, 48*1.5])

        #Objective help:
        text='Objective:'    #set the text
        renderedText = font2.render(text, 1, purple)          #render the text
        text_rect = renderedText.get_rect(center=(100, 200))  #set text align to center
        mainSurface.blit(renderedText, text_rect)             #display the text
        #set the texts:
        text = 'Your objective is to collect'
        text2 = 'all the coins in the maze'
        text3 = 'without being killed by the'
        text4 = 'enemies.'
        #render the texts:
        renderedText = font.render(text, 1, purple)
        renderedText2 = font.render(text2, 1, purple)
        renderedText3 = font.render(text3, 1, purple)
        renderedText4 = font.render(text4, 1, purple)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(100, 230))
        text_rect2 = renderedText2.get_rect(center=(100, 245))
        text_rect3 = renderedText3.get_rect(center=(100, 260))
        text_rect4 = renderedText4.get_rect(center=(100, 275))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        mainSurface.blit(renderedText3, text_rect3)
        mainSurface.blit(renderedText4, text_rect4)
     
        #Maze help:
        text='Maze:'    #set the text
        renderedText = font2.render(text, 1, blue)             #render the text
        text_rect = renderedText.get_rect(center=(300, 200))   #set text align to center
        mainSurface.blit(renderedText, text_rect)              #display the text
        #set the texts:
        text = 'You can change the maze'
        text2 = '(and its colour) in settings.'
        #render the texts:
        renderedText = font.render(text, 1, blue)
        renderedText2 = font.render(text2, 1, blue)
        #set text align to center:
        text_rect = renderedText.get_rect(center=(300, 230))
        text_rect2 = renderedText2.get_rect(center=(300, 245))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        
        #Turret help:
        text = 'Turret:'     #set the text
        renderedText = font2.render(text, 1, grey)           #render the text
        text_rect = renderedText.get_rect(center=(396, 20)) #set text align to center
        mainSurface.blit(renderedText, text_rect)           #display the text
        #set the texts:
        text = 'Turrets will shoot a laser every'
        text2 = 'certain amount of time. If their'
        text3 = 'laser hits you, you lose.'
        #render the texts:
        renderedText = font.render(text, 1, grey)           #render the text
        renderedText2 = font.render(text2, 1, grey)           #render the text
        renderedText3 = font.render(text3, 1, grey)           #render the text
        #set text align to center:
        text_rect = renderedText.get_rect(center=(396, 45)) 
        text_rect2 = renderedText2.get_rect(center=(396, 60))
        text_rect3 = renderedText3.get_rect(center=(396, 75))
        #display the texts:
        mainSurface.blit(renderedText, text_rect)
        mainSurface.blit(renderedText2, text_rect2)
        mainSurface.blit(renderedText3, text_rect3)

        mainSurface.blit(turret, (375, 97))
        
        pygame.display.flip()    #display the surface
        
        clock.tick(60)           #force the frame rate to be slower
#----------------
    
#WIN SCENE:
def win():
    pygame.init()      #prepare the pygame module for use
    surfaceSize = 480 
    
    clock = pygame.time.Clock()  #force the frame rate to be slower
    frameRate = 60

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    pygame.mixer.music.load('Win.mp3')    #load the sound
    pygame.mixer.music.play(0)            #play the sound
    pygame.mixer.music.unload             #unload the sound

    #load the fonts:
    font = pygame.font.Font('CrazytoonDemoRegular.ttf', 26)
    font2 = pygame.font.Font('CrazytoonDemoRegular.ttf', 75)
    font3 = pygame.font.SysFont('Arial Bold', 45)

    while True:  
        ev = pygame.event.poll()    #look for any event
        if ev.type == pygame.QUIT:  #window close button clicked...?
            pygame.quit()     #...close pygame
            sys.exit()        #...stop the program   
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #mouse button pressed down...?
            mouseX, mouseY = pygame.mouse.get_pos()    #get mouse position
            if mouseX >= 0 and mouseX <= 100 and mouseY >= 440 and mouseY <= 480:
                #mouse inside back to menu button...?
                menu()    #...start the menu scene    
            print(mouseX, mouseY)    #print the mouse position
            
        mainSurface.fill(black)     #draw the background   

        pygame.draw.rect(mainSurface, red, [0, 440, 100, 480])     #display main menu button background
        text = 'BACK'      #set the text
        renderedText = font.render(text, 1, black)     #render the text
        mainSurface.blit(renderedText, (13, 447))      #display the text

        text = 'YOU WIN'    #set the text
        renderedText = font2.render(text, 1, green)     #render the text
        mainSurface.blit(renderedText, (480/2-170, 480/2 - 100))      #display the text
        
        text = f'It took: {endTime} seconds'           #set the text
        renderedText = font3.render(text, 1, blue)     #render the text
        text_rect = renderedText.get_rect(center=(480/2, 275))    #set text align to center
        mainSurface.blit(renderedText, text_rect)      #display the text
        
        pygame.display.flip()    #display the surface
        
        clock.tick(frameRate)    #force the frame rate to be slower
#--------------------------------------
  
  
#LOSE SCENE:
def lose():
    pygame.init()      #pepare the pygame module for use
    surfaceSize = 480
    
    clock = pygame.time.Clock()  #force the frame rate to be slower
    frameRate = 60

    #create the surface with the size (surfaceSize[px] by surfaceSize[px])
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    pygame.mixer.music.load('Game_Over.mp3')     #load the sound
    pygame.mixer.music.play(0)                   #play the sound
    pygame.mixer.music.unload                    #unload the sound

    #load the fonts:
    font = pygame.font.Font('CrazytoonDemoRegular.ttf', 26)
    font2 = pygame.font.Font('CrazytoonDemoRegular.ttf', 75)
    font3 = pygame.font.SysFont('Arial Bold', 45)

    while True:  
        ev = pygame.event.poll()    #look for any events
        if ev.type == pygame.QUIT:  #window close button clicked...?
            pygame.quit()     #...close pygame
            sys.exit()        #...stop the program                  
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #mouse button pressed down...?
            mouseX, mouseY = pygame.mouse.get_pos()     #get the mouse position
            if mouseX >= 0 and mouseX <= 100 and mouseY >= 440 and mouseY <= 480:
                #mouse position inside back back to menu button...?
                menu()     #...start the menu scene
            print(mouseX, mouseY)     #print the mouse position
            
        mainSurface.fill(black)     #draw the background

        pygame.draw.rect(mainSurface, red, [0, 440, 100, 480])     #display the main menu button background
        text = 'BACK'     #set the text
        renderedText = font.render(text, 1, black)     #render the text
        mainSurface.blit(renderedText, (13, 447))      #display the text

        text = 'GAME OVER'     #set the text
        renderedText = font2.render(text, 1, red)     #render the text
        mainSurface.blit(renderedText, (480/2-232, 480/2 - 100))     #display the text
        
        text = f'You survived: {endTime} seconds'     #set the text
        renderedText = font3.render(text, 1, blue)    #render the text
        text_rect = renderedText.get_rect(center=(480/2, 275))     #set text align to center
        mainSurface.blit(renderedText, text_rect)     #display the text
        
        pygame.display.flip()     #display the surface
        
        clock.tick(frameRate)     #force the frame rate to be slower
#--------------------------------------
  

            
#MAZE:
#define mazeCoordinates, and add the inner coordinates
mazeCoordinates = [[9, 1], [2, 2], [3, 2], [5, 2], [6, 2], [7, 2], [9, 2], [11, 2], [12, 2], [13, 2], [15, 2], [16, 2], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4], [8, 4], [10, 4], [11, 4], [12, 4], [13, 4], [15, 4], [16, 4], [3, 5], [15, 5], [1, 6], [3, 6], [5, 6], [7, 6], [8, 6], [9, 6], [10, 6], [11, 6], [13, 6], [15, 6], [17, 6], [5, 7], [9, 7], [13, 7], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [9, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8]]

#add the ouline coordinates
def mazeOutline():
    global mazeCoordinates
    for i in range(0, 19):
        mazeCoordinates.append([i, 0])
        mazeCoordinates.append([i, 10])
    for i in range(1, 10):
        mazeCoordinates.append([0, i])
        mazeCoordinates.append([18, i])

def drawMaze(mainSurface, squareSize, color):
    #draw the acutal maze
       for i in range(0, len(mazeCoordinates)):
           #loop through each pair of coordinates in the current maze
           #than draw a square at each coordinate
        pygame.draw.rect(mainSurface, color, ((mazeCoordinates[i][0]*squareSize), (mazeCoordinates[i][1]*squareSize), squareSize, squareSize))

#all of the colors referenced in the code:
black = (0, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
orange = (255, 128, 0)
turqoise = (0, 255, 255)
sky = (0, 128, 255)
pink = (255, 0, 127)
lime = (173, 255, 47)
mint = (0, 250, 154)
beige = (255, 228, 196)
light_pink = (255, 192, 193)

#all the colors that the maze can be:
mazeColors = [black, grey, white, red, green, blue, purple, yellow, orange, turqoise, pink, sky, lime, mint, beige, light_pink]
mazeColor = 5      #current maze color index
#----------------------------------------