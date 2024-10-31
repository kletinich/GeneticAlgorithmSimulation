from SimpleWorld import SimpleWorld
import random
import time
import matplotlib.pyplot as plt

# The class that simulates the evolutional algorithm
class Evolution(object):
    def __init__(self):
        self.NUM_OF_SIMULATIONS = 10 # number of simulation in each generation
        self.NUM_OF_TURNS = 120 # number of turns until finishing simulation
        self.MAX_NUM_OF_GENERATIONS = 30 # the number of generation the algorithm will take
        
        self.__simulations = [SimpleWorld() for _ in range(self.NUM_OF_SIMULATIONS)] # the simulations
        self.__score = [0 for _ in range(self.NUM_OF_SIMULATIONS)] # the score of the simulation
        self.__maxAliveCellsInSimulations = [0 for _ in range(self.NUM_OF_SIMULATIONS)] #max alive cells in each simulation. Used to calculate the score
        self.__initialAliveCellsInSimulations = [0 for _ in range(self.NUM_OF_SIMULATIONS)] #initial alive cells in each simulation. Used to calculate the score
        self.__finishedAliveCellsInSimulations = [0 for _ in range(self.NUM_OF_SIMULATIONS)] # alive cells at the end in each simulation. Used to calculate the score
        self.__propability = [0 for _ in range(self.NUM_OF_SIMULATIONS)] # the propability of each simulation to be chosen to the next generation
        self.__generation = 0 # number of the generation
        self.__avg = 0 # average size of the current generation
        self.__bestScore = 0 # best score given to a simuation through all generations
        
        self.GREEN = '\033[32m'
        self.RESET = '\033[0m'
        
        plt.title("Average Number of alive cells in simulations")
        plt.xlabel("Generation")
        plt.ylabel("Average temperature change")
        plt.plot([self.__generation, 0], [0, 0])
       
    # generate a random first generation  
    def generateFirstGeneration(self):
        for i in range(self.NUM_OF_SIMULATIONS):
            self.__simulations[i].setStartingConfiguration()
      
    # return a random simulation
    def getRandomSimulation(self):
        sim = random.randint(0, self.NUM_OF_SIMULATIONS - 1)
        return sim
    
    # simulate a generation of simulations
    def simulateGeneration(self):
        self.__generation += 1
        print("Simulating generation " + str(self.__generation))
        startTime = time.time()
        
        for i in range(self.NUM_OF_SIMULATIONS):
            turnNum = 0
            scoreMultiplier = 0.1
            self.__initialAliveCellsInSimulations[i] = self.__simulations[i].getNumOfAliveCells() # for calculating the score
            
            for j in range(self.NUM_OF_TURNS):

                # one turn of the current simulation
                self.__simulations[i].turn(turnNum)
                turnNum += 1
                if(turnNum > 101):
                    check = self.__simulations[i].checkIfStabelized()
                    if(check):
                        scoreMultiplier = 1
                        break
                    
            self.__finishedAliveCellsInSimulations[i] = self.__simulations[i].getNumOfAliveCells()        
            self.__maxAliveCellsInSimulations[i] = self.__simulations[i].getMaxAliveCells()
            self.__score[i] = (self.__maxAliveCellsInSimulations[i] 
                               + self.__finishedAliveCellsInSimulations[i]
                               - self.__initialAliveCellsInSimulations[i]) * scoreMultiplier
         
        endTime = time.time()
        elapsed_time = endTime - startTime
        print("Time elapsed to simulate generation " + str(self.__generation) + ": " + str(elapsed_time) + " seconds")
        
    # calculate the propability of the simulation to be chosen, based on if they are metushelah and their maximum size
    def calculatePropabilityToBeChosen(self):
        totalScore = 0
        for i in range(self.NUM_OF_SIMULATIONS):
            totalScore += self.__score[i]
            
        for i in range(self.NUM_OF_SIMULATIONS):
            self.__propability[i] = self.__score[i]/totalScore
          
    # returns the best simulation out of all the simulations of the current generation
    def getBestSimulation(self):
        best = self.__simulations[0]
        bestScore = self.__score[0]
        index = 0
        
        for i in range(1, self.NUM_OF_SIMULATIONS):
            if(self.__score[i] > bestScore):
                bestScore = self.__score[i]
                best = self.__simulations[i]
                index = i
          
        # swapping so the best simulation will be first
        temp = self.__simulations[index]
        self.__simulations[index] = self.__simulations[0]
        self.__simulations[0] = temp
        
        temp = self.__maxAliveCellsInSimulations[index]
        self.__maxAliveCellsInSimulations[index] = self.__maxAliveCellsInSimulations[0]
        self.__maxAliveCellsInSimulations[0] = temp
        
        temp = self.__score[index]
        self.__score[index] = self.__score[0]
        self.__score[0] = temp 
        
        return best
    
    # mutate the current generation. The best simulation will mutate twice. return an array of the mutations
    def mutateGeneration(self):
        newGeneration = [0 for _ in range(self.NUM_OF_SIMULATIONS + 1)] # array of 2d arrays of the mutation
        
        # getting the best simulation, mutating it to 2 new mutations
        best = self.getBestSimulation()
        newGeneration[0] = best.getStartingWorld() 
        newGeneration[1] = best.getMutation() 
        
        for i in range(2, self.NUM_OF_SIMULATIONS + 1):
            newGeneration[i] = self.__simulations[i - 1].getMutation()
        newBestScore = self.__maxAliveCellsInSimulations[0]
        plt.plot([self.__generation - 1,self.__generation], [self.__bestScore, newBestScore])
        self.__bestScore = newBestScore
        return newGeneration
    
    # choose the next generation out of the mutations
    def chooseNextGeneration(self):
        mutations = self.mutateGeneration()
        chosen = [0 for _ in range(self.NUM_OF_SIMULATIONS)]
        self.__simulations[0].copyToStartingWorld(mutations[0]) 
        
        for i in range(1, self.NUM_OF_SIMULATIONS):
            chance = 0
            total = 1
            for j in range(0, self.NUM_OF_SIMULATIONS):
                rand = random.random()
                chance += self.__propability[j]
                
                if(rand < chance and not chosen[j]):
                    self.__simulations[i].copyToStartingWorld(mutations[j + 1])
                    chosen[j] = 1
                    total -= self.__propability[j]
                    self.__propability[j] = 0
                    
                    for k in range(self.NUM_OF_SIMULATIONS):
                        self.__propability[k] /= total
                        
                    break     
                  
        print("Generation " + str(self.__generation + 1) + " created")
        
    # print information about the generation
    def printGenerationInfo(self):
        print(self.GREEN + "Generation " + str(self.__generation) + " results:")
        print("max alive cells: " + str(self.__maxAliveCellsInSimulations)) 
        newAvg = 0
        for i in range(self.NUM_OF_SIMULATIONS):
            newAvg += self.__maxAliveCellsInSimulations[i]  
        newAvg /= self.NUM_OF_SIMULATIONS
        self.__avg = newAvg    
        print("Generation average max cells: " + str(newAvg))     
        print("score: " + str(self.__score))
        print(self.RESET)
    
    # print a simulation of the best world in the current generation
    def printBestSimulation(self):
        best = SimpleWorld()
        best.copyToStartingWorld(self.__simulations[0].getStartingWorld())
        print("Simulating best simulation:")
        time.sleep(4)
        for i in range(250):
            best.printWorld(i+1)
            best.turn(i+1)
            
    def openPlot(self):
        plt.title("Best simulation")
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.show()
     
    # simulate the whole algorithm for a few generations
    def startSimulations(self):
        self.generateFirstGeneration()
        for i in range(self.MAX_NUM_OF_GENERATIONS):
            self.simulateGeneration()
            self.calculatePropabilityToBeChosen()
            self.getBestSimulation()
            self.printGenerationInfo()
            self.chooseNextGeneration()
            self.printBestSimulation()
        self.openPlot()
         
        
        
        
                
               
                
                
               
                    
                 
                 
                 
      
        
        
        
        
            
        




