#GAsecond2
#---------------#
#Joshua Learn	#
#               #
# 11/17/14		#
#---------------#
MAX = 20
POP = 200
from math import sin
from random import randint


def createPopulation():
	M = ["".join([str(randint(0,1)) for c in range(MAX)]) for r in range(POP)]
	return M


def func(x,y):
	ans = x*sin(4*x) + 1.1*y*sin(2*y)
	return ans

def fitness(list1):

	maxVal = int('1111111111', 2)
	H = len(list1)//2
	x = int(list1[0:H], 2)
	y = int(list1[H:], 2)
	x = (x/maxVal)*10.0
	y = (y/maxVal)*10.0
	val = func(x, y)
	return val

def mate(list1, list2):
	splitPoint = randint(1,MAX)
	# print("split point: ", splitPoint)
	# printSeparator()
	firstChild = list1[1][0:splitPoint]+list2[1][splitPoint:]
	# print("FIRST: ", firstChild)
	secondChild = list2[1][0:splitPoint]+list1[1][splitPoint:]
	return ((fitness(firstChild),firstChild), (fitness(secondChild),secondChild),)

def evolve(population):
	
	alpha = population[0]
	newPopulation = []
	for i in range(1,101):
		children = mate(alpha, population[i])
		newPopulation.append(children[0])
		newPopulation.append(children[1])
	newPopulation.sort()
	return newPopulation


def printPopulation(population):
	for member in population:
		print(member[1], " fitness: ", member[0])
		printSeparator()
	print()
	print("-----------------------------< END OF PRINT POPULATION >-----------------------------------------------------")
	print()


def printSeparator():
	print("-------------------------------------------------------------------------------------------------------------")


def main():
	population = createPopulation()
	weightedPopulation = []
	for row in population:
		val = fitness(row)
		weightedPopulation.append((val, row))
	weightedPopulation.sort()
	for n in range(100):
		weightedPopulation = evolve(weightedPopulation)
	printPopulation(weightedPopulation)




main()

