import random
import operator

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
    for i in range(len(individual)):
        if (int(100 *random.random()) < 50):
            child += individual1[i]
        else:
            child += individual2[i]
    return child

def createChildren(breeders, number_of_children):
    nextPopulation = []
    for i in range(len(breeders//2)):
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
    return computerPerfPopulation(population, password)[0]

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

def main():
    

if __name__ == "__main__":
    main()