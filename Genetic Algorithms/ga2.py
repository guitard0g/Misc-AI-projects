#GA2
#Genetic Algorithm 
from random import choice, shuffle, randrange, random, randint;
import time
import matplotlib.pyplot as plt
#--------------< GLOBALS >------------------------------------
GENOMESIZE = 10
POPULATIONSIZE = 30
CHILDRENPRODUCED = 2
NUMOFEVOLUTIONS = int(input("How many Evolutions? "))
#-------------------------------------------------------------
	


def generatePopulation():
	population = []
	for i in range(POPULATIONSIZE):
		
		newArr = []
		for i in range(GENOMESIZE):
			rand =  choice([0,1,])
			newArr.append(rand)
		# print(newArr)
		population.append((fitness(newArr),newArr))
	# print(population)
	printSeparator()	
	return population


def fitness(list):
	if len(list)!=GENOMESIZE:
		print("DNA incorrect length.")
		return
	return sum(list)

def mate(list1, list2):
	splitPoint = randint(1,10)
	# print("split point: ", splitPoint)
	# printSeparator()
	firstChild = list1[1][0:splitPoint]+list2[1][splitPoint:]
	secondChild = list2[1][0:splitPoint]+list1[1][splitPoint:]
	if CHILDRENPRODUCED<2:
		return (firstChild,)
	return ((fitness(firstChild),firstChild), (fitness(secondChild),secondChild),)

def avgFitness(population):
    total = 0
    for member in population:
        total+=member[0]
    return total/len(population)
    
    
def printPopulation(population):
	for member in population:
		print(member[1])
		printSeparator()
	print()
	print("-----------------------------< END OF PRINT POPULATION >-----------------------------------------------------")
	print()

def printSeparator():
	print("-------------------------------------------------------------------------------------------------------------")

def evolve(population):
	population.sort()
	population.reverse()
	alpha = population[0]
	newPopulation = []
	for i in range(1,POPULATIONSIZE//2):
		children = mate(alpha, population[i])
		newPopulation.append(children[0])
		newPopulation.append(children[1])
	return newPopulation


def main():
    population = generatePopulation()
    population.sort()

    #printPopulation(population)
    for i in range(NUMOFEVOLUTIONS):
        plt.plot([i,], [avgFitness(population),], 'ro')
        population = evolve(population)
    plt.axis([0,NUMOFEVOLUTIONS,0,15])
    plt.xlabel('Number of Evolutions')
    plt.ylabel('Population Fitness')
    plt.show()
    #Population(population)
if __name__=='__main__': 
	main()


