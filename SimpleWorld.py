import random
import time

class SimpleWorld(object):
    def __init__(self):
        self.ROWS = 30
        self.COLUMNS = 30
        self.BASE_CHANCE_FOR_LIFE = 25 # chance that a cell will be generated as alive gor the first generation
        self.BASE_RAND_GEN = 100
        self.BASE_CHANCE_FOR_MUTATION = 10 # chance to toggle a cells status when mutating
        self.GREEN = '\033[32m'
        self.RESET = '\033[0m'
        
        self.__world = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] # world of cells
        self.__startingWorld = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] # the starting configuration of the world
        self.__checkLoop1 = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] # 1 check for stabilized game
        self.__checkLoop2 = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)] # 2 check for stabilized game
        
        self.__aliveCells = 0 # the current ammount of living cells
        self.__maxAliveCells = 0 # the maximum ammount of living cells presented in the game
        
        
    def getWorld(self):
        return self.__world
    
    def getStartingWorld(self):
        return self.__startingWorld
    
    def getNumOfAliveCells(self):
        return self.__aliveCells
    
    def getMaxAliveCells(self):
        return self.__maxAliveCells
    
    def getRows(self):
        return self.ROWS
    
    def getColumns(self):
        return self.COLUMNS
    
    def copyToStartingWorld(self, other):
        self.__aliveCells = 0
        self.__maxAliveCells = 0
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                self.__startingWorld[i][j] = other[i][j]
                self.__world[i][j] = other[i][j]
                self.__aliveCells += other[i][j]
    
    # set a random starting configuration for cells. Only for the first generation
    def setStartingConfiguration(self):
        for i in range((int)(self.ROWS/3), (int)(self.ROWS*2/3)):
            for j in range((int)(self.COLUMNS/3),(int)(self.COLUMNS*2/3)):
                chance = random.randint(1,self.BASE_RAND_GEN)
                if(chance < self.BASE_CHANCE_FOR_LIFE):
                    self.__startingWorld[i][j] = 1
                    self.__aliveCells += 1
                    
        for i in range((int)(self.ROWS/3), (int)(self.ROWS*2/3)):
            for j in range((int)(self.COLUMNS/3),(int)(self.COLUMNS*2/3)):
                self.__world[i][j] = self.__startingWorld[i][j]
                    
        self.__maxAliveCells = self.__aliveCells
        
    # count the number of alive neighbours of cell [i][j]
    def getNumOfAliveNeighbours(self, i, j):
        aliveNeighbours = 0
        
        if(i > 0 and self.__world[i-1][j] == 1):
            aliveNeighbours += 1
        if(i < self.ROWS - 1 and self.__world[i+1][j] == 1):
            aliveNeighbours += 1
        if(j > 0 and self.__world[i][j-1] == 1):
            aliveNeighbours += 1
        if(j < self.COLUMNS - 1 and self.__world[i][j+1] == 1):
            aliveNeighbours += 1
        if(i > 0 and j > 0 and self.__world[i-1][j-1] == 1):
            aliveNeighbours += 1
        if(i < self.ROWS - 1 and j > 0 and self.__world[i+1][j-1] == 1):
            aliveNeighbours += 1
        if(i > 0 and j < self.COLUMNS - 1 and self.__world[i-1][j+1] == 1):
            aliveNeighbours += 1
        if(i < self.ROWS - 1 and j < self.COLUMNS - 1 and self.__world[i+1][j+1] == 1):
            aliveNeighbours += 1
            
        return aliveNeighbours
    
    # 1 turn in the game
    def turn(self, turnNum):   
        tempWorld = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                aliveNeighbours = self.getNumOfAliveNeighbours(i, j)
                
                # alive cell will die because of underpopulation or overpopulation
                if((aliveNeighbours < 2 or aliveNeighbours > 3) and self.__world[i][j] == 1):
                    tempWorld[i][j] = 0
                    self.__aliveCells -= 1
                  
                # dead cell will be alive because of the right ammount of neighbours
                elif(aliveNeighbours == 3 and self.__world[i][j] == 0):
                    tempWorld[i][j] = 1
                    self.__aliveCells += 1
                
                # alive cell that has the right ammount of neighbours will be alive
                elif((aliveNeighbours == 2 or aliveNeighbours == 3) and self.__world[i][j] == 1):
                    tempWorld[i][j] = 1
        
        if(self.__aliveCells > self.__maxAliveCells):
            self.__maxAliveCells = self.__aliveCells
                    
        # after calculating the future state of the cells, update them
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                self.__world[i][j] = tempWorld[i][j]
        
        # setting a checker for a stabilized cells
        if(turnNum == 50):
            for i in range(self.ROWS):
                for j in range(self.COLUMNS):
                    self.__checkLoop1[i][j] = self.__world[i][j]
                    
        # setting a second checker for a stabilized cells         
        elif(turnNum == 100):
            for i in range(self.ROWS):
                for j in range(self.COLUMNS):
                    self.__checkLoop2[i][j] = self.__world[i][j]
                    
    # check if the current state of the cells is stable, comparing it to the checkers              
    def checkIfStabelized(self):
        check1 = True
        check2 = True
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if(check1 and self.__world[i][j] != self.__checkLoop1[i][j]):
                    check1 = False
                if(check2 and self.__world[i][j] != self.__checkLoop2[i][j]):
                    check2 = False
                    
                if(not check1 and not check2):
                    return False 
        return True
         
    # printing the state of the world                          
    def printWorld(self, turn):
        print("\033c", end="")
        print("Best simulation:")
        print(self)
        print("turn: " + str(turn) + " number of alive cells: " + str(self.__aliveCells) + " best: " + str(self.__maxAliveCells))
     
        time.sleep(0.05)
        
    # return a mutation of the current world
    def getMutation(self):
        self.__aliveCells = 0
        mutation = [[0 for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]
        
        for i in range((int)(self.ROWS/3), (int)(self.ROWS*2/3)):
            for j in range((int)(self.COLUMNS/3),(int)(self.COLUMNS*2/3)):
                mutation[i][j] = self.__startingWorld[i][j]
       
        for i in range((int)(self.ROWS/3), (int)(self.ROWS*2/3)):
            for j in range((int)(self.COLUMNS/3),(int)(self.COLUMNS*2/3)):
                chance = random.randint(1,self.BASE_RAND_GEN)
                if(chance < self.BASE_CHANCE_FOR_MUTATION):
                    mutation[i][j] = 1 - mutation[i][j]
                    
        return mutation

    # return a string that represents the world  
    def __str__(self):
        info = ""
        for i in range(self.ROWS):
            for j in range(self.COLUMNS):
                if(self.__world[i][j] == 1):
                    info += self.RESET + '*'
                else:
                    info += self.GREEN + '-'
                info += " "
            if(i < self.ROWS):
                info += "\n"
         
        info += self.RESET
        return info
 
        



