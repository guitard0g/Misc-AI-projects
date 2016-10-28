#GA2
#Genetic Algorithm 
from random import choice, shuffle, randrange, random, randint;
import time
import matplotlib.pyplot as plt
#--------------< GLOBALS >------------------------------------
GENOMESIZE = 20
POPULATIONSIZE = 35
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

def avgFitness(population):
    total = 0
    for member in population:
        total+=member[0]
    return total/len(population)
    
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

def differentiate(list1, list2):
	difference = 0
	for i in range(len(list1[1])):
		if list1[1][i] != list2[1][i]:
			difference+=1
	return difference

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
	copy = population[1:]
	differentiatedPopulation = []
	for member in copy:
		differentiatedPopulation.append(((differentiate(alpha, member)*0.5)+(member[0]*0.5), member[1]))
	differentiatedPopulation.sort()
	differentiatedPopulation.reverse()	
	for i in range(POPULATIONSIZE//2):
		children = mate(alpha, differentiatedPopulation[i])
		newPopulation.append(children[0])
		newPopulation.append(children[1])
	return newPopulation


def main():
    population = generatePopulation()
    population.sort()
    # printPopulation(population)
    for i in range(NUMOFEVOLUTIONS):
        plt.plot([i,], [avgFitness(population),], 'ro')
        population = evolve(population)
		# printPopulation(population)
		# time.sleep(0.4)
    plt.axis([0,NUMOFEVOLUTIONS,0,GENOMESIZE*1.5])
    plt.xlabel('Number of Evolutions')
    plt.ylabel('Population Fitness')
    plt.show()
	# tup = mate(population[0], population[1])
	# print(tup)
	#printPopulation(population)
if __name__=='__main__': 
	main()


