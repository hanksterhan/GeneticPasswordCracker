import random
import operator
import argparse
import matplotlib.pyplot as plt
import time

tempstart = time.time()

def generateAWord(length):
    i = 0
    result = ""
    while i < length:
        letter = chr(97 + int(26 * random.random()))
        result += letter
        i += 1
    return result

def generateFirstPopulation(sizePopulation, password):
    population = []
    i = 0
    while i < sizePopulation:
        population.append(generateAWord(len(password)))
        i += 1
    return population

def computePerfPopulation(population, password):
    populationPerf = {}
    for individual in population:
        populationPerf[individual] = fitness(password, individual)
    return sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=True)

def selectFromPopulation(populationSorted, best_sample, lucky_few):
    nextGeneration = []
    for i in range(best_sample):
        nextGeneration.append(populationSorted[i][0])
    for i in range(lucky_few):
        nextGeneration.append(random.choice(populationSorted)[0])
    random.shuffle(nextGeneration)
    return nextGeneration

def createChild(individual1, individual2):
    child = ""
    for i in range(len(individual1)):
        if (int(100 *random.random()) < 50):
            child += individual1[i]
        else:
            child += individual2[i]
    return child

def createChildren(breeders, number_of_children):
    nextPopulation = []
    for i in range(len(breeders)//2):
        for j in range(number_of_children):
            nextPopulation.append(createChild(breeders[i], breeders[len(breeders) - 1 - i]))
    return nextPopulation

def mutateWord(word):
    index_modification = int(random.random() * len(word))
    if (index_modification == 0):
        word = chr(97 + int(26 * random.random())) + word[1:]
    else:
        word = word[:index_modification] + chr(97 + int(26 * random.random())) + word[index_modification+1:]
    return word

def mutatePopulation(population, chance_of_mutation):
    for i in range(len(population)):
        if (random.random() * 100 < chance_of_mutation):
            population[i] = mutateWord(population[i])
    return population

def nextGeneration(firstGeneration, password, best_sample, lucky_few, number_of_children, chance_of_mutation):
    populationSorted = computePerfPopulation(firstGeneration, password)
    nextBreeders = selectFromPopulation(populationSorted, best_sample, lucky_few)
    nextPopulation = createChildren(nextBreeders, number_of_children)
    nextGeneration = mutatePopulation(nextPopulation, chance_of_mutation)
    return nextGeneration

def multipleGeneration(number_of_generation, password, size_population, best_sample, lucky_few, number_of_children, chance_of_mutation):
    historic = []
    historic.append(generateFirstPopulation(size_population, password))
    for i in range(number_of_generation):
        historic.append(nextGeneration(historic[i], password, best_sample, lucky_few, number_of_children, chance_of_mutation))
    return historic

def getBestIndividualFromPopulation(population, password):
    return computePerfPopulation(population, password)[0]

def getListBestIndividualFromHistorique(historic, password):
    bestIndividuals = []
    for population in historic:
        bestIndividuals.append(getBestIndividualFromPopulation(population, password))
    return bestIndividuals

def fitness(password, test_word):
    if (len(test_word) != len(password)):
        print("taille incompatible")
        return
    else:
        score = 0
        i = 0
        while (i <len(password)):
            if (password[i] == test_word[i]):
                score += 1
            i += 1
        return score * 100 / len(password)

def printResult(historic, password, number_of_generation):
    result = getListBestIndividualFromHistorique(historic, password)[number_of_generation-1]
    print ("solution: \"" + result[0] + "\", fitness: " + str(result[1]))

#graph
def evolutionBestFitness(historic, password):
    plt.axis([0,len(historic),0,105])
    plt.title(password)

    evolutionFitness = []
    for population in historic:
        evolutionFitness.append(getBestIndividualFromPopulation(population, password)[1])
    plt.plot(evolutionFitness)
    plt.ylabel('fitness best individual')
    plt.xlabel('generation')
    plt.show()

def evolutionAverageFitness(historic, password, size_population):
    plt.axis([0,len(historic),0,105])
    plt.title(password)

    evolutionFitness = []
    for population in historic:
        populationPerf = computePerfPopulation(population, password)
        averageFitness = 0
        for individual in populationPerf:
        	averageFitness += individual[1]
        evolutionFitness.append(averageFitness/size_population)
    plt.plot(evolutionFitness)
    plt.ylabel('Average fitness')
    plt.xlabel('generation')
    plt.show()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--password", required=True, help="The password to be cracked by the algorithm")
    parser.add_argument("-s", "--size_of_population", type=int, default=100, help="The size of the population")
    parser.add_argument("-l", "--lucky_few", type= int, default=20, help="The number of passwords to be randomly passed on in each generation")
    parser.add_argument("-b", "--best_sample", type=int, default=20, help="The number of the top passwords to be passed on in each generation")
    parser.add_argument("-c", "--num_children", type=int, default=5, help="The number of children in each generation")
    parser.add_argument("-n", "--num_generation", type=int, default=50, help="The number of generations in the algorithm")
    parser.add_argument("-m", "--chance_of_mutation", type=int, default=5, help="The percentage chance of mutation [0<m<100]")
    args = parser.parse_args()

    if ((args.best_sample + args.lucky_few) / 2 * args.num_children != args.size_of_population):
        print("pouplation size not stable")
    else:
        historic = multipleGeneration(args.num_generation, args.password, args.size_of_population, args.best_sample, args.lucky_few, args.num_children, args.chance_of_mutation)
        printResult(historic, args.password, args.num_generation)
        evolutionBestFitness(historic, args.password)
        evolutionAverageFitness(historic, args.password, args.size_of_population)
    print(time.time() - tempstart)

if __name__ == "__main__":
    main()
