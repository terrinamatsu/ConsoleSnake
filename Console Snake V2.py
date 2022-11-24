'''
    This is a simple, terminal-based version of the classic snake game.

    Written by Jacob Worgan, and based on the Snake code by Georgij Liasenko.
    For a personal project.
    Ver. 0.1, 29/9/2019 14:51
'''

#Imports
import random
import math as maths # <- important to rename it to maths, we're not american
import time
import keyboard

#Game settings
width = 5
height = 6
actingWidth = width+2
actingHeight = height+2
snake = '●'
snakeBody = '*'
fruit = '+'
space = ' '
boardTile = '_'
boardWall = 'x'
framesPerSecond = 2

#Main code
class BoardObj():
    ''' class that holds the values for the board '''
    def __init__(self, snakeHead, snakeBodies, snakeSegNo):
        # function to define the initial board
        self.map=[[boardWall]*actingWidth for i in range(actingHeight)]
        self.objectMap=[[space]*actingWidth for i in range(actingHeight)]

        self.fruit = [(0,0)]*10
        self.fruitNo = 0

        self.updateObjMap(snakeHead, snakeBodies, snakeSegNo)

        for i in range(1,actingHeight-1):
            for j in range(1,actingWidth-1):
                self.map[i][j]=boardTile

        self.addFruit()

    def printMap(self):
        #print the map array
        a=''
        
        for i in range(0,actingHeight):
            for j in range(0,actingWidth):
                if(self.objectMap[i][j] == space):
                    a+=self.map[i][j]
                else:
                    a+=self.objectMap[i][j]
                a+=' '
            print(a)
            a=''

    def updateObjMap(self, snakeHead, snakeBodies, snakeSegNo):
        # update the object map

        for i in range(0,actingHeight):
            for j in range(0,actingWidth):
                self.objectMap[i][j] = space

        #add fruit
        for i in range(0,self.fruitNo):
            self.objectMap[self.fruit[i][1]][self.fruit[i][0]] = fruit

        #add snake body
        for i in range(0,snakeSegNo):
            self.objectMap[snakeBodies[i][0]][snakeBodies[i][1]] = snakeBody

        #add snake head
        self.objectMap[snakeHead[0]][snakeHead[1]] = snake

    def collisions(self, snakeHead, snakeBody, snakeSegNo):
        # snake head/body collision
        for i in range(0,snakeSegNo):
            if snakeHead == snakeBody[i]:
                return 0

        # snake head/border collision
        if(snakeHead[0] <= 0) or (snakeHead[0] > height) or (snakeHead[1] <= 0) or (snakeHead[1] > width):
            return 0

        # snake head/fruit collision
        for i in range(0,self.fruitNo):
            if snakeHead == (self.fruit[i][1],self.fruit[i][0]):
                self.objectMap[self.fruit[i][1]][self.fruit[i][0]] = space
                for j in range(i,self.fruitNo):
                    self.fruit[j] = self.fruit[j+1]
                self.fruitNo-=1
                self.addFruit()
                return 2

        return 1

    def addFruit(self):
        a = 0
        while(a == 0):
            y = random.randint(1,height)
            x = random.randint(1,width)
            if (self.objectMap[y][x] == space):
                self.fruit[self.fruitNo] = (x,y)
                a = 1
        self.fruitNo += 1
        if(self.fruitNo == 2)or(self.fruitNo == 5)or(self.fruitNo == 8):
            self.addFruit()

            
class SnakeObj():
    ''' class that stores and handles the snake values '''
    def __init__(self):
        self.head = (random.randint(1,height),random.randint(1,width))
        self.body = [(0,0)]*(width * height)
        self.segNo = 0
        self.direction = 'q'
        print(self.head)

    def moveSnake(self):
        # snake body segments movement
        for i in range(self.segNo + 1,0,-1):
            self.body[i] = self.body[i-1]
        self.body[0] = self.head

        # snake head movement
        if(keyboard.is_pressed('a')) and (self.direction != 'd'):
            self.head = (self.head[0], self.head[1]-1)
            self.direction = 'a'
        elif(keyboard.is_pressed('d')) and (self.direction != 'a'):
            self.head = (self.head[0], self.head[1]+1)
            self.direction = 'd'
        elif(keyboard.is_pressed('s')) and (self.direction != 'w'): 
            self.head = (self.head[0]+1, self.head[1])
            self.direction = 's'
        elif(keyboard.is_pressed('w')) and (self.direction != 's'):
            self.head = (self.head[0]-1, self.head[1])
            self.direction = 'w'
        else:
            if(self.direction == 'a'):
                self.head = (self.head[0], self.head[1]-1)
            elif(self.direction == 'd'):
                self.head = (self.head[0], self.head[1]+1)
            elif(self.direction == 's'):
                self.head = (self.head[0]+1, self.head[1])
            elif(self.direction == 'w'):
                self.head = (self.head[0]-1, self.head[1])


    def addSegment(self):
        if self.segNo == 0:
            self.body[0] = self.head
        else:
            self.body[self.segNo] = self.body[self.segNo-1]
        
        self.segNo += 1
            
              
class MainWindow():
    ''' class that handles the main gameplay loop '''
    def __init__(self):
        # initialises the game
        self.snake = SnakeObj()
        self.board = BoardObj(self.snake.head, self.snake.body, self.snake.segNo)

        self.score = 0

        # starts main loop
        self.mainLoop()
        
    def mainLoop(self):
        # holds the main program loop
        end=0
        timer = time.time()

        while (end == 0):
            # delay based on frames per second
            if((time.time() - timer) > ((1 / framesPerSecond)-(self.score/100))):
                print('\n')
                
                # find key presses
                if(keyboard.is_pressed('q')):
                    end = 1

                self.snake.moveSnake()

                z = self.board.collisions(self.snake.head,self.snake.body,self.snake.segNo)

                if(z == 0):
                    end = 1
                elif(z == 2):
                    self.score+=1
                    self.snake.addSegment()

                self.board.updateObjMap(self.snake.head, self.snake.body, self.snake.segNo)
                self.board.printMap()
                timer = time.time()

                print(self.snake.segNo)
            elif keyboard.is_pressed('q'):
                end = 1

        print('Crash!!\nScore: '+str(self.score))
        
        
''' main program '''
if __name__=="__main__":
    # start game
    main = MainWindow()
    