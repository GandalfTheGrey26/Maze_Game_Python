import pygame, math
from variables_and_functions import *

global mazes, mazeLevel, allMazes, mazeCoordinates
mazes = 3        #amount of mazes
mazeLevel = 1    #the current maze
#the corrdinates of each maze:
allMazes = [
    [[9, 1], [2, 2], [3, 2], [5, 2], [6, 2], [7, 2], [9, 2], [11, 2], [12, 2], [13, 2], [15, 2], [16, 2], [2, 4], [3, 4], [5, 4], [6, 4], [7, 4], [8, 4], [10, 4], [11, 4], [12, 4], [13, 4], [15, 4], [16, 4], [3, 5], [15, 5], [1, 6], [3, 6], [5, 6], [7, 6], [8, 6], [9, 6], [10, 6], [11, 6], [13, 6], [15, 6], [17, 6], [5, 7], [9, 7], [13, 7], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [9, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [0, 0], [0, 10], [1, 0], [1, 10], [2, 0], [2, 10], [3, 0], [3, 10], [4, 0], [4, 10], [5, 0], [5, 10], [6, 0], [6, 10], [7, 0], [7, 10], [8, 0], [8, 10], [9, 0], [9, 10], [10, 0], [10, 10], [11, 0], [11, 10], [12, 0], [12, 10], [13, 0], [13, 10], [14, 0], [14, 10], [15, 0], [15, 10], [16, 0], [16, 10], [17, 0], [17, 10], [18, 0], [18, 10], [0, 1], [18, 1], [0, 2], [18, 2], [0, 3], [18, 3], [0, 4], [18, 4], [0, 5], [18, 5], [0, 6], [18, 6], [0, 7], [18, 7], [0, 8], [18, 8], [0, 9], [18, 9]],
    [[1, 1], [5, 1], [7, 1], [9, 1], [14, 1], [2, 2], [10, 2], [11, 2], [12, 2], [15, 2], [4, 3], [6, 3], [8, 3], [16, 3], [1, 4], [3, 4], [5, 4], [7, 4], [9, 4], [10, 4], [12, 4], [13, 4], [14, 4], [3, 5], [7, 5], [12, 5], [15, 5], [17, 5], [4, 6], [7, 6], [8, 6], [9, 6], [11, 6], [12, 6], [15, 6], [1, 7], [4, 7], [9, 7], [10, 7], [16, 7], [5, 8], [7, 8], [9, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [3, 9], [11, 9]],
    [[5, 1], [11, 1], [12, 1], [4, 2], [8, 2], [9, 2], [13, 2], [14, 2], [16, 2], [5, 3], [6, 3], [10, 3], [2, 4], [3, 4], [7, 4], [10, 4], [15, 4], [16, 4], [1, 5], [4, 5], [9, 5], [11, 5], [13, 5], [14, 5], [15, 5], [4, 6], [6, 6], [12, 6], [4, 7], [12, 7], [14, 7], [16, 7], [2, 8], [6, 8], [8, 8], [9, 8], [12, 8], [15, 8], [4, 9], [7, 9], [12, 9]]                                                   
    ]

class MenuSprite:
    def __init__(self, mainSurface, pos, alive, delayLength, color):
        self.mainSurface = mainSurface    #set the main surface
        self.scale = 1                    #set the scale
        
        #load the sprite sheet and scale it:
        self.spriteSheet = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/CHARACTER_SPRITES/{color}/Gunner_{color}_Run.png')
        self.spriteSheet = pygame.transform.smoothscale(self.spriteSheet, (self.scale*self.spriteSheet.get_width(),self.scale*self.spriteSheet.get_height()))
        
        self.rect = [0, 0, 288/6, 48]    #cutout of the sprite sheet
        self.pos = pos                   #position of the sprite
        self.delayLength = delayLength   #delay between animation of sprite
        self.patchNumber = 0             #current patch of sprite
        self.numPatches = 6              #number of patches in sprite sheet
        self.delay = 0                   #animation delay counter
        self.alive = alive               #sprite is alive
        self.shotDelay = 0               #sprites' shot delay is 0
        self.shot = False                #sprite is not currently 'shooting'
        self.doneShot = False            #sprite has not already 'shot'
    
    def draw(self):
        #animate the sprite
        if self.alive:
            #sprite is alive...?
            if self.delay == self.delayLength:
                #...animation is ready to change...?
                if (self.patchNumber < self.numPatches-1):
                    #...animation is NOT on the last patch...?
                    self.patchNumber += 1             #...add one to the patch
                    self.rect[0] += self.rect[2]      #...shift the sprite sheet cut out
                else:
                    self.patchNumber = 0            #...reset back to the first patch
                    self.rect = [0, 0, 288/6, 48]   #...reset the sprite sheet cutout
                self.delay = 0     #...reset the delay
            else:
                self.delay += 1    #...add one to the delay
                
            
            if self.pos[0] < 530:
                #sprite x-pos is less than 530...?
                self.pos[0] += 1    #...move the sprite to the right
            else:
                self.pos[0] = -50   #...reset the sprite x-pos

            #display the sprite:
            self.mainSurface.blit(self.spriteSheet, self.pos, self.rect)
            
            self.shotDelay += 1     #add one to the sprites shot delay
#-----------------------------------

class Bullet:
    def __init__(self, mainSurface, spritePos, othSpritePos):
        self.mainSurface = mainSurface      #set the main surface
        self.bulletPos=[spritePos[0] + 37, spritePos[1] + 16]    #set the position
        self.othSpritePos = othSpritePos    #set position of the other sprite
        
        #load the images of the 'bullet' and stream
        self.bulletSprite = pygame.image.load('C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/EXTRAS/SpongeBullet.png')
        self.streamSprite = pygame.image.load('C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/EXTRAS/BulletStream.png')

    def draw(self):
        if self.bulletPos[0] < 530:
            #bullet x-pos is less than 530...?
            for i in range(0, 10):
                #...loop through range 0 to 10
                self.bulletPos[0] += 1    #increse bullet x-pos by one
                
                #draw the bullet and strem:
                self.mainSurface.blit(self.bulletSprite, self.bulletPos, [0, 0, 3, 1])
                self.mainSurface.blit(self.streamSprite, (self.bulletPos[0]-20, self.bulletPos[1] - 7), [0, 0, 80, 16])
                
                if self.bulletPos[0] == self.othSpritePos[0]:
                    #bullet position is the same as the other sprite...?
                    return True    #return that the bullet HAS hit the other sprite
#----------------------------------------
                
class Player:
    def __init__(self, mainSurface, playerCoordinates, scale, playerRect, playerColor, squareSize, mazeLvl):        
        self.mazeCoords = allMazes[mazeLvl - 1]    #set the current maze coordinates
        self.scale = scale                         #set the scale 
        self.squareSize = squareSize               #set the size of each maze square
        self.mainSurface = mainSurface             #set the main surface
        self.playerCoordinates = playerCoordinates #set the player coordinates
        self.playerRect = playerRect               #set the cutout of the sprite sheet
        self.direction = 'right'                   #set the player to facing right
        self.blocked = False                       #set the player to not blocked (by the maze)
        self.playerPatchNumber = 0                 #set the player patch to 0
        self.playerNumPatches = 5                  #set the number of patches to 5
        self.delay = True                          #set the player animation delay to true
        
        #set the player position based on the player coordinates and square size:
        self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
        
        #load the sprite sheet and transform it:
        self.spriteSheet = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/CHARACTER_SPRITES/{playerColor}/Gunner_{playerColor}_Idle.png')
        self.spriteSheet = pygame.transform.smoothscale(self.spriteSheet, (self.scale*self.spriteSheet.get_width(),self.scale*self.spriteSheet.get_height()))
        
    def drawPlayer(self):
        #update the player position based on the player coordinates and square size:
        self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
        
        if self.delay == False:
            #animation delay is false...?
            if (self.playerPatchNumber < self.playerNumPatches-1):
                #...not on last sprite sheet cutout...?
                self.playerPatchNumber += 1               #...add one to the patch
                self.playerRect[0] += self.playerRect[2]  #...shift the sprite sheet cutout     
            else:
                self.playerPatchNumber = 0      #...reset back to the first patch
                self.playerRect = [0, 0, self.scale*48, self.scale*48]   #...reset the sprite sheet cutout
            self.delay = True    #...set the delay to true
        elif self.delay == True:
            #delay is true...?
            self.delay = False   #...set it to false
            
        #display the player:
        self.mainSurface.blit(self.spriteSheet, self.playerPos, self.playerRect)

    def movePlayer(self, key):
        '''
            Move the player in a certain direction.
            
            Take the key that has been pressed, and use it to determine
            a direction. Check if that direction is blocked.
            
            Returns
            -------
            boolean
                returns wether the player can (True) move, or can't (False) move
            
        '''
        
        
        if key == pygame.K_w:
            #w is pressed...?
            barrier = False    #...assume that the player isn't blocked
            for i in range(0, len(self.mazeCoords)):
                #loop through the maze coordinates
                if self.playerCoordinates[0] == self.mazeCoords[i][0] and self.playerCoordinates[1] == self.mazeCoords[i][1] + 1:
                    #player can not move...?
                    barrier = True    #...player is blocked
                    break             #...break out of the loop
            if barrier == False:
                #player can move...?
                self.playerCoordinates[1] -= 1    #...move the player
                
                #...update the player position based on the player coordinates and square size
                self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
                
                #...display the player
                self.mainSurface.blit(self.spriteSheet, self.playerPos, self.playerRect)    
        if key == pygame.K_a:
            #see line 147 to 164
            if self.direction != 'left':
                self.direction = 'left'
                self.spriteSheet = pygame.transform.flip(self.spriteSheet, True, False)
            barrier = False
            for i in range(0, len(self.mazeCoords)):
                if self.playerCoordinates[1] == self.mazeCoords[i][1] and self.playerCoordinates[0] == self.mazeCoords[i][0] + 1:
                    barrier = True
                    break
            if barrier == False:
                self.playerCoordinates[0] -= 1
                self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
                self.mainSurface.blit(self.spriteSheet, self.playerPos, self.playerRect)        
        if key == pygame.K_s:
            #see line 147 to 164
            barrier = False
            for i in range(0, len(self.mazeCoords)):
                if self.playerCoordinates[0] == self.mazeCoords[i][0] and self.playerCoordinates[1] == self.mazeCoords[i][1] - 1:
                    barrier = True
                    break
            if barrier == False:
                self.playerCoordinates[1] += 1
                self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
                self.mainSurface.blit(self.spriteSheet, self.playerPos, self.playerRect)
        if key == pygame.K_d:
            #see line 147 to 164
            if self.direction != 'right':
                self.direction = 'right'
                self.spriteSheet = pygame.transform.flip(self.spriteSheet, True, False)
            barrier = False
            for i in range(0, len(self.mazeCoords)):
                if self.playerCoordinates[1] == self.mazeCoords[i][1] and self.playerCoordinates[0] == self.mazeCoords[i][0] - 1:
                    barrier = True
                    break
            if barrier == False:
                self.playerCoordinates[0] += 1
                self.playerPos = [self.squareSize*self.playerCoordinates[0], self.squareSize*self.playerCoordinates[1]]
                self.mainSurface.blit(self.spriteSheet, self.playerPos, self.playerRect)  
#----------------------------------------
        
#ENEMY AI:    
class Enemy:
    def __init__(self, mainSurface, scale, enemyRect, enemyColor, squareSize, mazeLvl):
        self.mazeCoords = allMazes[mazeLvl - 1]    #set the current maze coordinates
        self.squareSize = squareSize               #set the square size
        self.enemyColor = enemyColor               #set the enemy color
        self.scale = scale                         #set the enemy scale
        self.mainSurface = mainSurface             #set the main surface
        self.direction = 'right'                   #set the enemy to facing right
        while True:
            #give the enemy random coordinates until they are not inside the walls of the maze
            self.enemyCoordinates = [(random.randint(1, 16)), (random.randint(1, 8))]
            if self.enemyCoordinates not in self.mazeCoords:
                break
        self.enemyRect = enemyRect                 #set the cutout of the sprite sheet 
        self.blocked = False                       #assume that the enemy is not blocked
        self.enemyPatchNumber = 0                  #set the current patch to 0
        self.enemyNumPatches = 5                   #set the number of patches to 5
        self.delay = True                          #set the animation delay to true
        
        #set the enemy position based on the coordinates and square size
        self.enemyPos = [self.squareSize*self.enemyCoordinates[0], self.squareSize*self.enemyCoordinates[1]]
        
        #load and transform the sprite sheet:
        self.spriteSheet = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/CHARACTER_SPRITES/{self.enemyColor}/Gunner_{self.enemyColor}_Idle.png')
        self.spriteSheet = pygame.transform.smoothscale(self.spriteSheet, (self.scale*self.spriteSheet.get_width(),self.scale*self.spriteSheet.get_height()))

                                      
    def drawEnemy(self):
        #set the enemy postion based on the coordinates and square size
        self.enemyPos = [self.squareSize*self.enemyCoordinates[0], self.squareSize*self.enemyCoordinates[1]]

        if self.delay == False:
            #animation delay is true...?
            if (self.enemyPatchNumber < self.enemyNumPatches-1):
                #...not on last patch...?
                self.enemyPatchNumber += 1              #...add one to the patch
                self.enemyRect[0] += self.enemyRect[2]  #...shift the sprite sheet cutout
            else:
                self.enemyPatchNumber = 0     #...reset back to the first patch
                self.enemyRect = [0, 0, self.scale*48, self.scale*48]  #reset the sprite sheet cutout
            self.delay = True    #...set animation delay to true
        elif self.delay == True:
            #animation delay is true...?
            self.delay = False    #...set animation delay to false
            
        #display the enemy:
        self.mainSurface.blit(self.spriteSheet, self.enemyPos, self.enemyRect)

    def enemyBarrierCheck(self, direction):
        '''
          This function checks to see if the an enemy is able to move in a
          certain direction.
          
          Using: the coordinates of the enemy, the current maze coordinates
          (self.mazeCoords), and an inputed direction; this function returns
          whether the enemy is able to move in a certain direction.

          Parameters
          ----------
          self.enemyCoordinates : list
            list of the two enemy coordinates [x, y]
          direction : string
            the direction that is being checked
          self.mazeCoords : list
            a list of all the coordinates of the physical maze [[x, y], [x, y]...]
          
          Returns
          -------
          boolean
            returns wether the enemy can (True) move, or can't (False) move
        '''
        bar = False          #Initialize the (enemy_Is_)bar(red) variable as False
        if direction == 'right':
            for i in range(0, len(self.mazeCoords)):     #loop through all maze coordinates
                #enemy is left one value of current maze coordinates...?
                if self.enemyCoordinates[0] == self.mazeCoords[i][0] - 1 and self.enemyCoordinates[1] == self.mazeCoords[i][1]:
                    bar = True     #...enemy is barred
                    break          #break out of the loop
        elif direction == 'left':
            for i in range(0, len(self.mazeCoords)):     #loop through all maze coordinates
                #enemy is one value right of current maze coordinates...?
                if self.enemyCoordinates[0] == self.mazeCoords[i][0] + 1 and self.enemyCoordinates[1] == self.mazeCoords[i][1]:
                    bar = True     #...enemy is barred
                    break          #break out of loop
        elif direction == 'up':
            for i in range(0, len(self.mazeCoords)):     #loop through all maze coordinates
                #enemy is one value below of current maze coordinates...?
                if self.enemyCoordinates[0] == self.mazeCoords[i][0] and self.enemyCoordinates[1] == self.mazeCoords[i][1] + 1:
                    bar = True     #...enemy is barred
                    break          #break out of loop
        elif direction == 'down':
            for i in range(0, len(self.mazeCoords)):     #loop through all maze coordinates
                #enemy is one value above current maze coordinates...?
                if self.enemyCoordinates[0] == self.mazeCoords[i][0] and self.enemyCoordinates[1] == self.mazeCoords[i][1] - 1:
                    bar = True     #...enemy is barred
                    break          #break out of loop
        
        if bar == False:     #enemy is not barred in given direction...?
            return False     #...return that enemy is not barred
        else:
            return True      #...else return enemy is barred

    def moveEnemy(self, playerCoordinates):
        '''
          Move enemy towards player
          
          Checks which direction the enemy needs to move (to go towards
          the player), and uses the 'enemyBarrierCheck()' function to see
          if the enemy can move in that direction. Update the enemy
          coordinates and direction based on results. (Does NOT physically
          change the enemies position on the screen).

          Parameters
          ----------
          playerCoordinates : list
            the coordinates [(0 to 18), (0 to 10)] of the player
          enemyCoordinates : list
            the coordinates [(0 to 18), (0 to 10)] of the enemy
          enemyDirection : string
            the direction the enemy is facing (right or left)
          (enemy)spriteSheet : image
            the actual sprite sheet of the enemy
          
          Returns
          -------
          None
        '''
        if self.enemyCoordinates[0] < playerCoordinates[0] and self.enemyBarrierCheck('right') == False:
            #enemy needs to move right and is not blocked...?
            self.enemyCoordinates[0] += 1     #...add one to the enemy x-coordinate
            if self.direction != 'right':
                #enemy is not already facing right...?
                self.direction = 'right'     #...set the enemy direction variable to right
                self.spriteSheet = pygame.transform.flip(self.spriteSheet, True, False)     #...physicaly flip the sprite sheet so it faces right
        elif self.enemyCoordinates[0] > playerCoordinates[0] and self.enemyBarrierCheck('left') == False:
            #...elif enemy needs to move left and is not blocked...?
            self.enemyCoordinates[0] -= 1     #...remove one from the enemy x-coordinate
            if self.direction != 'left':
                #enemy is not already facing left...?
                self.direction = 'left'     #...set the enemy direction variable to left
                self.spriteSheet = pygame.transform.flip(self.spriteSheet, True, False)     #...physicaly flip the sprite sheet so it faces left
        elif self.enemyCoordinates[1] < playerCoordinates[1] and self.enemyBarrierCheck('down') == False:
            #enemy needs to move down and is not blocked...?
            self.enemyCoordinates[1] += 1     #...add one to the enemy y-coordinate 
        elif self.enemyCoordinates[1] > playerCoordinates[1] and self.enemyBarrierCheck('up') == False:
            #enemy needs to move up and is not blocked...?
            self.enemyCoordinates[1] -= 1     #...remove one from the enemy y-coordinate

    def updateEnemy(self):
        '''
            Updates the enemyPos(ition) variable so that it is an actual
            set of coordinates on the physical screen. enemyPos is what
            is used when 'drawing' the enemy on the screen.
        '''
        #Takes the enemyCoordinates, than scales them based on the square size
        self.enemyPos = [self.squareSize*self.enemyCoordinates[0], self.squareSize*self.enemyCoordinates[1]]
#------------------------------------------

class Coin:
    def __init__(self, mainSurface, scale, squareSize, mazeLvl):
        self.mazeCoords = allMazes[mazeLvl - 1]    #set the current maze coordinates
        self.squareSize = squareSize               #set the square size
        self.scale = scale                         #set the scale
        self.mainSurface = mainSurface             #set the main surface
        self.coinRect = [0, 0, (700/6)*self.scale, 200*self.scale]    #set the sprite sheet cutout   
        self.coinNumPatches = 6                    #set the number of patches to 6
        self.coinPatchNumber = 0                   #set the current patch to 0
        self.delay = True                          #set the animation delay to true
        self.collected = False                     #set the coin to not collected
        while True:
            #randomly set the coin coordinates until they aren't inside the maze walls (or inside player)
            self.coinCoordinates = [(random.randint(1, 16)), (random.randint(1, 9))]
            if self.coinCoordinates not in self.mazeCoords and self.coinCoordinates != [9, 9]:
                break
            
        #set the coin position based on the coordinates and square size
        self.coinPos = [self.squareSize*self.coinCoordinates[0], self.squareSize*self.coinCoordinates[1]]
        
        #load the sprite sheet and transform it
        self.spriteSheet = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/Spinning_Coin.png')
        self.spriteSheet = pygame.transform.smoothscale(self.spriteSheet, (self.scale*self.spriteSheet.get_width(),self.scale*self.spriteSheet.get_height()))
    
    def drawCoin(self):
        '''
          Draw the coin on the screen.
          
          Using a delay (to reduce animation speed), animate the coin
          (spinning), and draw it on the screen.
        '''
        if self.delay == False:
            #animation delay is false...?
            if (self.coinPatchNumber < self.coinNumPatches-1):
                #...not the last patch...?
                self.coinPatchNumber += 1             #...add one to the patch
                self.coinRect[0] += self.coinRect[2]  #...shift the sprite sheet cutout
            else:
                self.coinPatchNumber = 0          #...reset back to first patch
                self.coinRect = [0, 0, (700/6)*self.scale, 200*self.scale]   #...reset the sprite sheet cutou
            self.delay = True    #...set delay to true
        elif self.delay == True:
            #delay is true...?
            self.delay = False    #...set delay to false
            
        #display the coin:
        self.mainSurface.blit(self.spriteSheet, self.coinPos, self.coinRect)
#-------------------------------------
        
class Turret:
    def __init__(self, mainSurface, coords, delayLength, squareSize, direction):
        self.mainSurface = mainSurface    #set the main surface
        self.squareSize = squareSize      #set the square size        
        self.coords = coords              #set the coordinates of the turret
        self.pos = [self.coords[0] * squareSize, self.coords[1] * squareSize]  #set the position of the turret based on the square size and coordinates
        self.shotDelayLength = delayLength     #delay between shots
        self.shotCounter = 0                   #shot delay counter                   
        self.direction = direction             #set the direction of the turret
        self.shooting = False                  #set the turret to not currently shooting
        
        #load the turret sprite sheet:
        self.spriteSheet = pygame.image.load(f'C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/Turret.png')

        if self.direction == 'right':
            #turret is facing right...?
            self.laserPos=[self.pos[0] + 37, self.pos[1] + 5]     #...set the laser position 
        else:
            self.laserPos=[self.pos[0] - 37, self.pos[1] + 5]    #...set the laser position

        #load the images of the laser and stream
        self.laserSprite = pygame.image.load('C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/EXTRAS/SpongeBullet.png')
        self.streamSprite = pygame.image.load('C:/Users/Glenn/Pictures/Saved Pictures/PyGame_Sprites/gunner/EXTRAS/LaserStream.png')

    def draw(self):
        '''
          Display the turret and add to the shot counter.
        '''
        self.mainSurface.blit(self.spriteSheet, self.pos)     #display the turret
        if self.shooting == False:
            #...turrent isn't currently shooting...?
            self.shotCounter += 1     #...add one to the shot counter

    def flip(self):
        #flip the sprite sheet so that the turret faces the correct direction
        self.spriteSheet = pygame.transform.flip(self.spriteSheet, True, False)
            
    def shoot(self, playerPos):
        '''
           Draw the turret laser.
           
           Draw the laser until it is off the screen OR until
           it hits the player, in which case return that the
           player has (True) been hit.
        '''
        if self.direction == 'right':
            #turret is facing right...?
            if self.laserPos[0] < 530:
                #laser x-pos is less than 530...?
                for i in range(0, 10):
                    #...loop through range 0 to 10
                    self.laserPos[0] += 1    #increse laser x-pos by one
                    
                    #display the laser and laser stream:
                    self.mainSurface.blit(self.laserSprite, self.laserPos, [0, 0, 3, 1])
                    self.mainSurface.blit(self.streamSprite, (self.laserPos[0]-20, self.laserPos[1] - 7), [0, 0, 80, 16])
                    
                    #calculate the distance between  the laser and player using pythagorean theorem: dist = sqrt(((x2 - x1)^2) + ((y2 - y1)^2))
                    x = ((self.laserPos[0] - playerPos[0]) ** 2)
                    y = ((self.laserPos[1] - playerPos[1]) ** 2)
                    dist = math.sqrt((x + y))
                    
                    if dist <= 15:
                        #distance is less or equal to 15...?
                        return True      #...return that the player has been hit

            else:
                self.shooting = False    #...turret is no longer shooting
                self.shotCounter = 0     #...reset turret counter
        else:
            #...turret is facing left...?
            if self.laserPos[0] >= -50:
                #laser x-pos is greater than -50...?
                for i in range(0, 10):
                    #...loop through range 0 to 10
                    self.laserPos[0] -= 1    #decrease laser x-pos by one
                    
                    #display the laser and strem:
                    self.mainSurface.blit(self.laserSprite, self.laserPos, [0, 0, 3, 1])
                    self.mainSurface.blit(self.streamSprite, (self.laserPos[0]-20, self.laserPos[1] - 7), [0, 0, 80, 16])
                    
                    #calculate the distance between  the laser and player using pythagorean theorem: dist = sqrt(((x2 - x1)^2) + ((y2 - y1)^2))
                    x = ((self.laserPos[0] - playerPos[0]) ** 2)
                    y = ((self.laserPos[1] - playerPos[1]) ** 2)
                    dist = math.sqrt((x + y))
                    
                    if dist <= 15:
                        #distance is less than equal to 15...?
                        return True     #...return that the player has been hit
            else:
                self.shooting = False    #...turret is no longer shooting
                self.shotCounter = 0     #...reset turret counter
#---------------------------------------------