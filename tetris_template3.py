###############################################################################
# Name:
#  _____              _      _   _  __     _       _                   _    _ 
# |  __ \            (_)    | | | |/ /    | |     | |                 | |  (_)
# | |  | | __ _ _ __  _  ___| | | ' /_   _| | __ _| | _____  _   _ ___| | ___ 
# | |  | |/ _` | '_ \| |/ _ \ | |  <| | | | |/ _` | |/ / _ \| | | / __| |/ / |
# | |__| | (_| | | | | |  __/ | | . \ |_| | | (_| |   < (_) | |_| \__ \   <| |
# |_____/ \__,_|_| |_|_|\___|_| |_|\_\__,_|_|\__,_|_|\_\___/ \__,_|___/_|\_\_|
# Due Date: December 13, 2016
# Description: Tetris Template #3
###############################################################################

from tetris_classes3 import * #imports all necessary files, modules, etc
from random import randint
import pygame
import time
pygame.init() #initiates pygame

HEIGHT = 600 #declares the screen variables
WIDTH  = 800
GRIDSIZE = 30
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (95,95,95)

introScreen = True #makes the intro screen true

fontSize=40 #declares the font variables
font = pygame.font.SysFont("Arial Black",fontSize) # create a variable font

#declares the playing field dimensions
#---------------------------------------#
COLUMNS = 10                            #
ROWS = 20                               # 
LEFT = 8.2                              # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = -1                                #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

#loads and resizes all of the images
darkBlue = pygame.image.load("darkBlue.png")
darkBlue = darkBlue.convert_alpha()
darkBlue = pygame.transform.scale(darkBlue, (20,20))

lightBlue = pygame.image.load("lightBlue.png")
lightBlue = lightBlue.convert_alpha()
lightBlue = pygame.transform.scale(lightBlue, (20,20))

red = pygame.image.load("red.png")
red = red.convert_alpha()
red = pygame.transform.scale(red, (20,20))

purple = pygame.image.load("purple.png")
purple = purple.convert_alpha()
purple = pygame.transform.scale(purple, (20,20))

green = pygame.image.load("green.png")
green = green.convert_alpha()
green = pygame.transform.scale(green, (20,20))

yellow = pygame.image.load("yellow.png")
yellow = yellow.convert_alpha()
yellow = pygame.transform.scale(yellow, (20,20))

orange = pygame.image.load("orange.png")
orange = orange.convert_alpha()
orange = pygame.transform.scale(orange, (20,20))

background = pygame.image.load("background.png")
background = background.convert_alpha()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))

intro = pygame.image.load("introPage.png")
intro = intro.convert_alpha()
intro = pygame.transform.scale(intro, (800,600))

playButton = pygame.image.load("button.png")
playButton = playButton.convert_alpha()
playButton = pygame.transform.scale(playButton, (180,50))

hover = pygame.image.load("hover.png")
hover = hover.convert_alpha()
hover = pygame.transform.scale(hover, (180,50))

insButton = pygame.image.load("button.png")
insButton = insButton.convert_alpha()
insButton = pygame.transform.scale(insButton, (180,50))

play = pygame.image.load("play.png")
play = play.convert_alpha()
play = pygame.transform.scale(play, (WIDTH,HEIGHT))

instructions = pygame.image.load("instructions.png")
instructions = instructions.convert_alpha()
instructions = pygame.transform.scale(instructions, (WIDTH,HEIGHT))

pauseScreen = pygame.image.load("pauseScreen.png")
pauseScreen = pauseScreen.convert_alpha()
pauseScreen = pygame.transform.scale(pauseScreen, (WIDTH,HEIGHT))

gameOverScreen = pygame.image.load("gameOverScreen.png")
gameOverScreen = gameOverScreen.convert_alpha()
gameOverScreen = pygame.transform.scale(gameOverScreen, (WIDTH,HEIGHT))

#declares the score and line variables
lines = 0
score = 0
stage = 1

#makes pause, four rows, etc false
pause = False
oneFourRows = False
gameOver = False

#declares the game modes which control the speed of the program
easy = 15
medium = 8
hard = 5

mode = easy

gameDelay = mode

#time variables
timeee = 0
unPauseTime = 0

#frames
frames = 0

#---------------------------------------#
#   functions                           #
#---------------------------------------#

#music files
pygame.mixer.music.load("backgroundMusic.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops = -1)

move = pygame.mixer.Sound("move.wav")
rotate = pygame.mixer.Sound("rotate.wav")
oneRow = pygame.mixer.Sound("oneRow.wav")
fourRowsOnce = pygame.mixer.Sound("fourRowsOnce.wav")
fourRowsTwice = pygame.mixer.Sound("fourRowsTwice.wav")
drop = pygame.mixer.Sound("drop.wav")
down = pygame.mixer.Sound("down.wav")

#intro screen
def introooooo():
    global timeeeeeeeee
    timeeeeeeeee = time.clock()
    
    screen.blit(intro, (0,0))
    screen.blit(playButton, (290,404))

    (cursorX,cursorY)=pygame.mouse.get_pos()
    if(cursorX>290 and cursorX<470 and cursorY>404 and cursorY<450):
        screen.blit(hover, (290,404))
    
    screen.blit(play,(110,0))

#background
def draw_background():
    global tim
    #time variables
    if(gameOver==False):
        if(pause==False):
            if(introScreen==True): #time before the game starts is taken away
                tim = int(time.clock()-timeeeeeeeee)
            else:
                tim = int(time.clock()-unPauseTime) #time while paused is taken away
    
    screen.blit(background, (-3,0)) #background
    
    #makes the fade effect
    rect = pygame.Surface((300,570), pygame.SRCALPHA, 32)
    rect.fill((0, 0, 0, 20))
    screen.blit(rect, (247,0))

    #lines variable
    linnnnnnnes = font.render(str(lines), 1, (255,255,255))
    screen.blit(linnnnnnnes,(620,330))

    #score variable
    sccccccore = font.render(str(score), 1, (255,255,255))
    screen.blit(sccccccore,(620,480))

    #stage variable
    staaaaaaaage = font.render(str(stage), 1, (255,255,255))
    screen.blit(staaaaaaaage,(620,40))

    #time variables
    timee = font.render(str(tim)+" s", 1, (255,255,255))
    screen.blit(timee, (620,190))

#grid
##    for i in range(COLUMNS+1):
##        pygame.draw.line(screen, ((200-(i*9)),(200-(i*1)),(200-(i*1))), (i*GRIDSIZE+LEFT*GRIDSIZE,TOP*GRIDSIZE),(i*GRIDSIZE+LEFT*GRIDSIZE,TOP*GRIDSIZE+21*GRIDSIZE),2)
##    for i in range(ROWS+1):
##        pygame.draw.line(screen, ((200-(i*9)),(200-(i*1)),(200-(i*9))), (LEFT*GRIDSIZE,i*GRIDSIZE+TOP*GRIDSIZE),(LEFT*GRIDSIZE+14*GRIDSIZE,i*GRIDSIZE+TOP*GRIDSIZE),2)

#pause function
def pauseeeeee(): #displays the pause screen
    screen.blit(pauseScreen,(-3,0))

#game over function
def gameOverrrrrrrrrr():
    screen.blit(gameOverScreen,(0,0))
    gg = font.render("Press 'R' To Restart", 1, (255,255,255))
    screen.blit(gg,((WIDTH/2)-230,(HEIGHT/2)+100))

#redraw function
def redraw_screen():
    #draws the intro screen if the intro screen is needed
    if(introScreen==True):
        introooooo()
    else: #draws the background and all the shapes
        draw_background() #background, timer, etc
        nextShape.draw(screen, GRIDSIZE) #next shape
        holdShape.draw(screen, GRIDSIZE) #held shape
        shape.draw(screen, GRIDSIZE) #actual shape
        floor.draw(screen, GRIDSIZE) #grid
        top.draw(screen, GRIDSIZE)
        leftWall.draw(screen, GRIDSIZE)
        rightWall.draw(screen, GRIDSIZE)
        obstacles.draw(screen, GRIDSIZE)
        shadow.draw(screen, GRIDSIZE) #shadow
        if(pause==True): #goes to the pause function is true
            pauseeeeee()
        if(gameOver==True):
            gameOverrrrrrrrrr()
    pygame.display.update()

#---------------------------------------#
#   main program                        #
#---------------------------------------#

#random shape are assigned
shapeNo = randint(1,7)
nextShapeNo = randint(1,7)
holdNo = randint(1,7)

#the line is slightly off so it is drawn differently
#next shape
if(nextShapeNo!=5):
    nextShape = Shape(3,4.8,nextShapeNo)
else:
    nextShape = Shape(2.5, 4.8, nextShapeNo)

#held shape
if(holdNo!=5):
    holdShape = Shape(-3,-13.1,holdNo)
else:
    holdShape = Shape(-2.5,-13.1, holdNo)

#declares all the figures, floor, sides, etc
shape = Shape(MIDDLE,TOP,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
top = Floor(LEFT, TOP, COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obstacles = Obstacles(LEFT, FLOOR)
shadow = Shadow(MIDDLE, TOP, shapeNo)

inPlay = True                                       
#plays while inPlay is true and it quits if it isn't
while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #detects the user exits the program       
            inPlay = False       
        if event.type == pygame.KEYDOWN: #checks if keys are pressed
            if event.key == pygame.K_UP and pause==False and gameOver==False:                    
                shape.rotateClkwise() #does the same thing to the shadow as to the shape
                shadow.rotateClkwise()
                rotate.play()
                if(shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(obstacles)):
                    shape.rotateCntclkwise() #undoes the last action if collision occurs
                    shadow.rotateCntclkwise()
            if event.key == pygame.K_LEFT and pause==False and gameOver==False:
                shape.move_left()
                shadow.move_left()
                move.play()
                if shape.collides(leftWall) or shape.collides(obstacles):
                    shape.move_right()
                    shadow.move_right()
            if event.key == pygame.K_RIGHT and pause==False and gameOver==False:
                shape.move_right()
                shadow.move_right()
                move.play()
                if shape.collides(rightWall) or shape.collides(obstacles):
                    shape.move_left()
                    shadow.move_left()

            if event.key == pygame.K_LSHIFT and pause==False and gameOver==False: #holds the shape when pressing the left shift button
                if(holdNo!=0):
                    holdNo,shapeNo = shapeNo,holdNo #switches the values of shape number and hold number
                    shape = Shape(shape.col,shape.row,shapeNo) #draws the shapes
                    shadow = Shadow(shape.col, shape.row, shapeNo)
                    
                    if(shape.collides(leftWall)): #moves the shape if there is a collision
                        shape.move_right()
                        shadow.move_right()
                    elif(shape.collides(rightWall)):
                        shape.move_left()
                        shadow.move_left()
                else: #if there is not shape held, a random shape is given
                    holdNo,shapeNo = shapeNo,randint(1,7)

                    if(shape.collides(leftWall)): #moves the shape if there is a collision
                        shape.move_right()
                        shadow.move_right()
                    elif(shape.collides(rightWall)):
                        shape.move_left()
                        shadow.move_left()
                    
                if(holdNo!=5): #draws the held shape
                    holdShape = Shape(3,13.1,holdNo)
                else:
                    holdShape = Shape(2.5, 13.1, holdNo)


            if event.key == pygame.K_r and pause==False and gameOver==True: #restarts if game over
                pygame.mixer.music.load("backgroundMusic.wav") #resets all variables except for running time
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops = -1)
                obstacles.blocks = []
                lines = 0
                score = 0
                stage = 0
                mode = easy
                shapeNo = randint(1,7)
                nextShapeNo = randint(1,7)
                holdNo = randint(1,7)

                if(nextShapeNo!=5):
                    nextShape = Shape(3,4.8,nextShapeNo)
                else:
                    nextShape = Shape(2.5, 4.8, nextShapeNo)

                if(holdNo!=5):
                    holdShape = Shape(-3,-13.1,holdNo)
                else:
                    holdShape = Shape(-2.5,-13.1, holdNo)

                shape = Shape(MIDDLE,TOP,shapeNo) #draws all the shapes
                obstacles = Obstacles(LEFT, FLOOR)
                shadow = Shadow(MIDDLE, TOP, shapeNo)
                
                gameOver=False                    #makes game over false
            
            if event.key == pygame.K_SPACE and pause==False and gameOver==False: #drops the shape down when space is pressed
                while(shape.collides(floor)==False and shape.collides(obstacles)==False): #keeps moving the shape down until it collides
                    shape.move_down()
                shape.move_up()

            if event.key == pygame.K_p and pause==False and gameOver==False: #pauses the game
                pause = True
                pauseTime = time.clock()
            elif event.key == pygame.K_p and pause==True and gameOver==False:
                unPauseTime = time.clock()-pauseTime
                pause = False
                
            if event.key == pygame.K_DOWN and pause==False and gameOver==False: #makes the shape go down faster
                mode-=1
                shape.move_down()
                if(shape.collides(floor) or shape.collides(obstacles)):
                    shape.move_up()
                    mode+=1
            else:
                if(score<500):
                    mode = easy
                elif(score>=500 and score<1000): #increases the speed and stage depending on the score
                    stage = 2
                    mode = medium
                elif(score>=1000):
                    stage = 3
                    mode = hard

        if (event.type == pygame.MOUSEBUTTONDOWN and introScreen==True): #detects if the play button has been pressed
            (cursorX,cursorY)=pygame.mouse.get_pos()
            if(cursorX>290 and cursorX<470 and cursorY>404 and cursorY<450):
                introScreen = False
                
    if(introScreen==False and pause==False and gameOver==False and frames%mode==0): #drops the shape down depending on the game mode           
        shape.move_down()
        if (shape.collides(floor) or shape.collides(obstacles)): #stops the shape from going through the bottom or obstacles
            shape.move_up()
            drop.play()
            obstacles.append(shape)
            fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS)    # finds the full rows and removes their blocks from the obstacles 

            if(len(fullRows)>=1 and len(fullRows)<4): #if less than three rows are cleared, score only increases by 100
                lines+=len(fullRows)
                score+=100*len(fullRows)
                oneRow.play()
                oneFourRows = False
            elif(len(fullRows)>=4 and oneFourRows == False): #if four or more rows are cleared once, you get 800 points
                lines+=len(fullRows)
                score+=800
                score+=100*len(fullRows)
                fourRowsOnce.play()
                oneFourRows = True
            elif(oneFourRows == True and len(fullRows)>=4): #if four more rows are cleared in a row, you get 1200 points
                lines+=len(fullRows)
                score+=1200
                score+=100*len(fullRows)
                fourRowsTwice.play()

            if(score>=500 and score<1000): #increases the speed and stage depending on the score
                stage = 2
                mode = medium
            elif(score>=1000):
                stage = 3
                mode = hard

            obstacles.removeFullRows(fullRows) #removes the full rows
            score+=10 #increase the score by ten whe the block is placed
            shapeNo = nextShapeNo #the shape becomes the nezt shape number
            nextShapeNo = randint(1,7) #the next shape is random
            shadow = Shadow(MIDDLE, TOP, shapeNo) #draws the shadow
            shape = Shape(MIDDLE,TOP,shapeNo) #draws the shape
            if(nextShapeNo!=5): #draws the next shape
                nextShape = Shape(3,4.8,nextShapeNo)
            else:
                nextShape = Shape(2.5, 4.8, nextShapeNo)

        if(shape.collides(obstacles) and (shape.row<5)): #if the obstacles get too high, you lose
            pygame.mixer.music.stop() #plays the game over music
            pygame.mixer.music.load("gameOverMusic.wav")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops = -1)
            gameOver=True

    shadow.row = 0 #drops the shadow to the lowest it can go
    while(shadow.collides(floor)==False and shadow.collides(obstacles)==False):
        shadow.move_down()
    shadow.move_up()

    redraw_screen() #redraws the screen
    frames+=1 #counts the frames
    pygame.time.delay(0) #doesn't delay the game
    
pygame.quit()
