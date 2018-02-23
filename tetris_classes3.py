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

#declares all the screen variables
import pygame
HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#loads all the images
darkBlue = pygame.image.load("darkBlue.png")
darkBlue = darkBlue.convert_alpha()
darkBlue = pygame.transform.scale(darkBlue, (30,30))

lightBlue = pygame.image.load("lightBlue.png")
lightBlue = lightBlue.convert_alpha()
lightBlue = pygame.transform.scale(lightBlue, (30,30))

red = pygame.image.load("red.png")
red = red.convert_alpha()
red = pygame.transform.scale(red, (30,30))

purple = pygame.image.load("purple.png")
purple = purple.convert_alpha()
purple = pygame.transform.scale(purple, (30,30))

green = pygame.image.load("green.png")
green = green.convert_alpha()
green = pygame.transform.scale(green, (30,30))

yellow = pygame.image.load("yellow.png")
yellow = yellow.convert_alpha()
yellow = pygame.transform.scale(yellow, (30,30))

orange = pygame.image.load("orange.png")
orange = orange.convert_alpha()
orange = pygame.transform.scale(orange, (30,30))

shadowBlock = pygame.image.load("shadowBlock.png")
shadowBlock = shadowBlock.convert_alpha()
shadowBlock = pygame.transform.scale(shadowBlock, (30,30))

#declares all the colours
BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255)
#array of colours
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
FIGURES   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object): #block class which draws the anchor block                   
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self): #string method                 
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        if(CLR == RED): #draws the corresponding image depending on the colour
            surface.blit(red, (x,y))
        elif(CLR == GREEN):
            screen.blit(green, (x,y))
        elif(CLR == BLUE):
            screen.blit(darkBlue, (x,y))
        elif(CLR == ORANGE):
            screen.blit(orange, (x,y))
        elif(CLR == CYAN):
            screen.blit(lightBlue, (x,y))
        elif(CLR == MAGENTA):
            screen.blit(purple, (x,y))
        elif(CLR == YELLOW):
            screen.blit(yellow, (x,y))
        #pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        #pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 2)

    def move_down(self): #moves the block down               
        self.row = self.row + 1 


#---------------------------------------#
class Cluster(object): #cluster class which draws the rest of the blocks
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo

    def _update(self): #updates the screen by drawing the whole figure
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize): #draws the shapes by each block                   
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other): #detects any collisions
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): #appends the blocks
        """ Append all blocks from another cluster to this one.
        """
        for i in other.blocks:
            self.blocks.append(i)

#---------------------------------------#
class Obstacles(Cluster): #obstacles class which is formed by the placed pieces
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def findFullRows(self, top, bottom, columns): #finds all the full rows on the field
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows): #removes any full rows
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
   
#---------------------------------------#
class Shape(Cluster): #shape class which determines how the shapes are rotated and look                    
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate() # private
        
    def __str__(self):                  
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self): #shape rotates by moving the other blocks around the anchor point
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [-1, 0, 1, 1], [0, 0, 0,1], [-1, -1, 0, 1]]
            _rowOffsets = [[-1,-1, 0, 1], [0, 0, 0, -1], [-1, 0, 1, 1], [0, 1, 0, 0]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() # private

    def move_left(self): #moves in directions               
        self.col = self.col - 1                   
        self._update() # private
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() # private
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() # private
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() # private

    def rotateClkwise(self): #rotates the shape
        self._rot = ((self._rot + 1)%4)
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot + 3)%4  
        self._rotate()

#---------------------------------------#
class Floor(Cluster): #floor (top and bottom grid)
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i 
        self._update() # private       
            
#---------------------------------------#
class Wall(Cluster): #wall (left and right grid)
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update() # private Make sure all the methods marked as private have an underscore before its name


class ShadowBlock(object): #draws the shadow anchor block                   
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):#string method                 
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20): #draws the anchor block                    
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        screen.blit(shadowBlock, (x,y))
        #pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        #pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 2)

    def move_down(self):                
        self.row = self.row + 1

class ShadowCluster(object): #shadow cluster
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [ShadowBlock()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo

    def _update(self): #updates the screen by drawing the whole figure
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i]= ShadowBlock(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize): #draws each block                    
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other): #detects any collisions
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False

class Shadow(ShadowCluster): #draws the actual shadow                    
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate() # private
        
    def __str__(self): #string method                 
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self): #rotates by moving the blocks around the anchor point
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [-1, 0, 1, 1], [0, 0, 0,1], [-1, -1, 0, 1]]
            _rowOffsets = [[-1,-1, 0, 1], [0, 0, 0, -1], [-1, 0, 1, 1], [0, 1, 0, 0]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() # private

    def move_left(self): #moves the shadow               
        self.col = self.col - 1                   
        self._update() # private
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() # private
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() # private
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() # private

    def rotateClkwise(self): #rotates the shadow
        self._rot = ((self._rot + 1)%4)
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot + 3)%4  
        self._rotate()
