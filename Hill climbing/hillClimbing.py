#hill Climber

#---------------#
#Joshua Learn	#
#               #
# 11/17/14		#
#---------------#

from random import random, uniform, choice, randint
from math import sin, cos, atan2, tan, radians, degrees, pi
import matplotlib.pyplot as plt
def func(x,y):
	if x<=0 or x>=10 or y<=0 or y>=10:
		return float('inf')
	return x * sin(4 * x) + 1.1 * y * sin(2 * y)

def frange(start, stop, step):
	i = start
	terminate = stop-(step/10)
	while i<terminate:
		yield i 
		i+=step

# ---------------------------------------------------------------------------
def coorGenerator(maxx):
	for x in range(maxx):
		for y in range(maxx):
			yield x, y
# ---------------------------------------------------------------------------

def genSineTable():
	dic = {}
	for t in frange (0, 2*pi, 2*pi/64):
		dic[t] = sin(t)
	return dic


def genCosTable():
	dic = {}
	for t in frange (0, 2*pi, 2*pi/64):
		dic[t] = cos(t)
	return dic


def main():
	# INITIALIZE
    bestX = float('inf')
    bestY = float('inf')
    sinDic = genSineTable()
    cosDic = genCosTable()
    radius = 10
    x = random()*10
    y = random()*10
    bestF = func(bestX, bestY)
	#-----------------------------------------------------------------------
	

#	for t in frange (0, 2*pi, 2*pi/64):
#		trialX = x+radius*sinDic[t]
#		trialY = y+radius*cosDic[t]
#		trialF = func(trialX, trialY)
#		if trialF < bestF:
#			bestY = trialY
#			bestX = trialX
#			bestF = trialF

#    for trialX, trialY in coorGenerator(10):
#        trialF = func(trialX, trialY)
#        if trialF < bestF:
#            bestY = trialY
#            bestX = trialX
#            bestF = trialF
##            plt.plot([i1,], [avgFitness(population),], 'ro')

    for i in range(1000000):
        trialX = random()*10
        trialY = random()*10
        trialF = func(trialX, trialY)
        if trialF < bestF:
            bestY = trialY
            bestX = trialX
            bestF = trialF

    print()
    print()
    print()

    print("bestX, bestY, bestF: ", round(bestX,2), " ", round(bestY,2), " ", round(bestF,2), " ")
    print()
    print()
    print()

main()