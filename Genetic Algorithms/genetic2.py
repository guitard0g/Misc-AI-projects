#---------------#
#Joshua Learn	#
#               #
# 4/9/15 		#
#---------------#

#---------------------------------------------------
from random import random, uniform, choice, randint
from math import sin, cos, atan2, tan, radians, degrees
POP = 12
MAX = 20
#---------------------------------------------------

def main():
	population = createPopulation()
	population = sortPopulation(population)

	while(not populationIsStable(population)):
		population = evolvePopulation(population)

def f(x, y):
	return x * sin(4 * x) + 1.1 * y * sin(2 * y)

def evolvePopulation(population):
	newPopulation = []

	print("------< OLD POPULATION > ------")
	printPopulation(population)
	newPopulation = mateThePopulation(population)
	newPopulation = sortPopulation(newPopulation)
	print()

	print("------< NEW POPULATION > ------")
	printPopulation(newPopulation)
	print()

	print("###############################")
	print()
	return newPopulation

def createPopulation():
	population = []

	for pop in range(POP):
		genome = [''.join(str(randint(0,1)) for c in range(MAX))]
		genome = (calculateFitness(genome[0]), genome)
		population.append(genome)
	return population

def calculateFitness(genome):
	maxVal = int('1111111111', 2)
	x = int(genome[:10], 2)
	y = int(genome[10:], 2)
	x = (x/maxVal)*10.0
	y = (y/maxVal)*10.0
	# print("x")
	# print(x)
	# print("y")
	# print(y)
	# x = binate(x)
	# y = binate(y)

	return f(x, y)

def binate(binary):
	total = 0
	bi = binary[::-1]
	for i in range(len(binary)):
		if bi[i] == '1':
			total += 2**i
	return (total / 1023 * 10)

def mateThePopulation(population):
	newPop = []

	for i in range(1, int(POP/2)):
		childMale, childFemale = mate(population[0][1], population[i][1])
		newPop.append(childMale)
		newPop.append(childFemale)
	newPop = sorted(newPop, reverse=False)	
	return newPop

def mate(genomeMale, genomeFemale):
	split = randint(1,MAX)
	childMale = genomeMale[:split] + genomeFemale[split:]
	childMale = (calculateFitness(childMale), childMale)
	childFemale = genomeFemale[:split] + genomeMale[split:]
	childFemale = (calculateFitness(childFemale), childFemale)

	return (childMale, childFemale)

def sortPopulation(population):
	return sorted(population, reverse=False)

def printPopulation(population):
	for i in population:
		print("Fitness: ", i[0], "|", "Genome: ", i[1])
		print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

def populationIsStable(population):
	key = population[0][0]
	for i in population:
		if i[0] != key:
			return False
	return True
main()
main()