import random
import operator
import time

class PasswordCracker():
    def __init__(self):
        self.historic = None

    def generateAWord(self, length):
        """ Given a length, generate a word of that length
            input: length - int
            output: string of length length
        """
        i = 0 
        result = ""
        while i < length:
            letter = chr(97 + int(26 * random.random()))
            result += letter
            i += 1
        return result
    
    def generateFirstPopulation(self, sizePopulation, password):
        """ Given the size of the population and the password, generate a 
            generation of passwords using the length of the password
            input:  sizePopulation - int
                    password - str
            output: list of strings of size sizePopulation, each str of length password
        """
        population = []
        i = 0
        while i <sizePopulation:
            population.append(self.generateAWord(len(password)))
            i += 1
        return population
    
    def computePerfPopulation(self, population, password):
        """ Given a population and password, calculate the fitness of each member in the population
            and return a sorted list of descending fitness
            input:  population - list of strings
                    password - string
            output: population sorted by descending fitness
        """
        populationPerf = {}
        for individual in population:
            populationPerf[individual] = self.fitness(password, individual)
        return sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=True)

    def selectFromPopulation(self, populationSorted, best_sample, lucky_few):
        """ Given a sorted population, return the most fit members and a couple of random lucky members to act as parents for the next generation
            input:  populationSorted - sorted list of strings
                    best_sample - int denoting how many of the most fit members to select
                    lucky_few - int denoting how many random members to select
            output: randomized list of strings to pass on to the next generation
        """
        nextGeneration = []
        for i in range(best_sample):
            nextGeneration.append(populationSorted[i][0])
        for i in range(lucky_few):
            nextGeneration.append(random.choice(populationSorted)[0])
        random.shuffle(nextGeneration)
        return nextGeneration
    
    def createChild(self, individual1, individual2):
        """ Given two member strings, create a child by randomly selecting a character from each parent
            to pass on to the child
            input:  individual1 - string
                    individual2 - string
            output: string of length individual1
        """
        child = ""
        for i in range(len(individual1)):
            if (int(100 * random.random()) < 50):
                child += individual1[i]
            else:
                child += individual2[i]
        return child

    def createChildren(self, breeders, number_of_children):
        """ Given the parents and the number of children, create a generation of children 
            by calling the createChild() function
            input:  breeders - list of strings that will be the parents of the subsequent generation
                    number_of_children - int denoting how many children to have in the subsequent generation
            output: list of strings denoting the subsequent population
        """ 
        nextPopulation = []
        for i in range(len(breeders) // 2):
            for j in range(number_of_children):
                nextPopulation.append(self.createChild(breeders[i], breeders[len(breeders) - 1 - i]))
        return nextPopulation

    def mutateWord(self, word):
        """ Given a word, mutate a random letter within it
            input:  word - string
            output: string of the same length of word
        """
        index_modification = int(random.random() * len(word))
        if (index_modification == 0):
            word = chr(97 + int(26 * random.random())) + word[1:]
        else: 
            word = word[:index_modification] + chr(97 + int(26*random.random())) + word[index_modification+1:]
        return word

    def mutatePopulation(self, population, chance_of_mutation):
        """ Given a population and a chance of mutation, randomly mutate members in the populaton if the chance of mutation threshold is hit
            input:  population - list of strings
                    chance_of_mutation - int between 0 and 100 denoting the percentage chance of mutation
            output: list of strings denoting the population
        """
        for i in range(len(population)):
            if (random.random() * 100 < chance_of_mutation):
                population[i] = self.mutateWord(population[i])
        return population

    def nextGeneration(self, firstGeneration, password, best_sample, lucky_few, number_of_children, chance_of_mutation):
        """ Given the first Generation and a couple metrics, return the next generation
            output: the next generation of passwords
        """
        populationSorted = self.computePerfPopulation(firstGeneration, password)
        nextBreeders = self.selectFromPopulation(populationSorted, best_sample, lucky_few)
        nextPopulation = self.createChildren(nextBreeders, number_of_children)
        nextGeneration = self.mutatePopulation(nextPopulation, chance_of_mutation)
        return nextGeneration

    def multipleGeneration(self, number_of_generation, password, size_population, best_sample, lucky_few, number_of_children, chance_of_mutation):
        """ Given the metrics to specify the genetic algorithm, run the genetic algorithm, keeping track of the generations in historic
            output: historic - a list of lists where each sublist is a generation in the algorithm
        """
        historic = []
        historic.append(self.generateFirstPopulation(size_population, password))
        for i in range(number_of_generation):
            historic.append(self.nextGeneration(historic[i], password, best_sample, lucky_few, number_of_children, chance_of_mutation))
        self.historic = historic
        return historic
    
    def getBestIndividualFromPopulation(self, population, password):
        """ return the member from the generation that has the highest fitness score
            input:  population - list of strings, population in question
                    password - string
            output: string - password with the highest fitness score in a generation
        """
        return self.computePerfPopulation(population, password)[0]

    def getListBestIndividualFromHistorique(self, historic, password):
        """ Given a list of all the generations, return a list of members that each represent the highest fitness score 
            in their population/generation
            input:  historic - list of lists containing all the generations in the genetic algorithm
                    password - string
            output: a list of strings denoting the member with the highest fitness score in each generation
        """
        bestIndividuals = []
        for population in historic:
            bestIndividuals.append(self.getBestIndividualFromPopulation(population, password))
        return bestIndividuals
    
    def fitness(self, password, test_word):
        """ Given the password and a string, calculate the fitness of the string
            input:  password - target string
                    test_word - test string
            output: float representing the fitness score of the test_word
        """
        if (len(test_word) != len(password)):
            print("taille incompatible")
            return
        else: 
            score = 0
            i = 0
            while (i < len(password)):
                if (password[i] == test_word[i]):
                    score += 1
                i += 1
            return score * 100 / len(password)
    
    def returnResult(self, historic, password, number_of_generation):
        result = self.getListBestIndividualFromHistorique(historic, password)[number_of_generation-1]
        return ("The best result from the Genetic Algorithm was: \"" + result[0] + "\", with a fitness of: " + str(result[1]))
