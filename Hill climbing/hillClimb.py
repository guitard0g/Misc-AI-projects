#hill Climber

#---------------#
#Josh Learn  	#
#               #
# 11/17/14		#
#---------------#

from random import random, uniform, choice, randint
from math import sin, cos, atan2, tan, radians, degrees, pi
import math

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

def findG(A, B, C):
	x = (2*A[0]+B[0]+C[0])/4
	y = (2*A[1]+B[1]+C[1])/4
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x, y)

def findD(A, B, C):
	x = B[0]+C[0]-A[0]
	y = B[1]+C[1]-A[1]
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x,y)

def findE(A, B, C):
	x = (3*B[0]+3*C[0]-4*A[0])/2
	y = (3*B[1]+3*C[1]-4*A[1])/2
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x,y)

def findF(A, B, C):
	x = (3*B[0]+3*C[0]-2*A[0])/4
	y = (3*B[1]+3*C[1]-2*A[1])/4
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x,y)

def findH(A, B, C):
	x = (A[0]+B[0])/2
	y = (A[1]+B[1])/2
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x,y)

def findM(A, B, C):
	x = (C[0]+B[0])/2
	y = (C[1]+B[1])/2
	if x<0:
		x = 0
	if x>10:
		x = 10
	if y<0:
		y=0
	if y>10:
		y=10
	return (x,y)

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def main():
	# INITIALIZE -----------------------------------------------------
	bestX = float('inf')
	bestY = float('inf')
	bestF = float('inf')
	radius = 10
	# END OF INITIALIZATION -------------------------------------------

	#--------< NELDER MEAD ALGORITHM >---------------------------------
	
	for i in range(1000): #RUN ALGORITHM STARTING IN 100 DIFFERENT RANDOM SPOTS
		x = random()*10
		y = random()*10
		A = (x,y)
		x = random()*10
		y = random()*10
		B = (x,y)
		x = random()*10
		y = random()*10
		C = (x,y)
		cF =func(C[0], C[1])

		bF =func(B[0], B[1])

		aF =func(A[0], A[1])

		points = [(aF, A), (bF, B), (cF, C)]
		points.sort()
		A = points[2][1]
		C = points[1][1]
		B = points[0][1]
		cF =func(C[0], C[1])

		bF =func(B[0], B[1])

		aF =func(A[0], A[1])

		# for i in range(100): # FOR EACH RANDOM SPOT, GO THROUGH 100 ROUNDS OF THE ALGORITHM 
		while True:		
				br = False
				oldA = A
				# A = Worst point
				# B = Best point
				# C = Middle point
				
				# Put the previous points A, B, and C in order from best to worst, 
				# then re-choose your A, B, and C
				points = [(aF, A), (bF, B), (cF, C)] 
				points.sort()

				A = points[2][1]
				C = points[1][1]
				B = points[0][1]
				
				cF =func(C[0], C[1])
				bF =func(B[0], B[1])
				aF =func(A[0], A[1])
				#-----------------------------------------------------------------------------

				# used to check if none of our new points were valuable
				cont = True
				#---------------------------------------------------------------------------

				#ALGORITHM: Check D, then E, then F and G, then, if all  else fails, move A to H and C to M
				
				# Check 
				D = findD(A,B,C)
				dF = func(D[0], D[1])
				E = findE(A, B, C)
				eF = func(E[0], E[1])
				
				if dF < bF:
					if eF < dF:
						A = E
						aF = eF
					else:
						A = D
						aF= dF
				
				else:
					G = findG(A, B, C)
					gF = func(G[0], G[1])
					F = findF(A,B,C)
					fF = func(F[0], F[1])
					if gF < aF and gF < fF:
						A = G
						aF = gF
					elif fF <aF and fF <gF:
						A = F
						aF = fF
					else:
						cont = False
				
				if cont:
					H = findH(A,B,C)
					hF = func(H[0], H[1])

					M = findM(A,B,C)
					mF = func(M[0], M[1])

					A = H
					aF = hF
					C = M
					cF = mF
				if distance(oldA, A) <0.01:
					br = True
				if br:
					break
		if bF < bestF:

			bestF = bF
			bestX = B[0]
			bestY = B[1]

	#--------< END OF NELDER MEAD ALGORITHM >--------------------------
	

	#-----------------------------------------------------------------------
	
	#USE LOOKUP TABLE ------------------------------------------------------
	# sinDic = genSineTable()
	# cosDic = genCosTable()
	# for t in frange (0, 2*pi, 2*pi/64):
	# 	trialX = x+radius*sinDic[t]
	# 	trialY = y+radius*cosDic[t]
	# 	trialF = func(trialX, trialY)
	# 	if trialF < bestF:
	# 		bestY = trialY
	# 		bestX = trialX
	# 		bestF = trialF
	#----------------------------------------------------------------------

	#GENERATE GRID --------------------------------------------------------
	# for trialX, trialY in coorGenerator(10):
	# 	trialF = func(trialX, trialY)
	# 	if trialF < bestF:
	# 		bestY = trialY
	# 		bestX = trialX
	# 		bestF = trialF
	#----------------------------------------------------------------------

	#RANDOM POINTS --------------------------------------------------------
	# for i in range(1000000):
	# 	trialX = random()*10
	# 	trialY = random()*10
	# 	trialF = func(trialX, trialY)
	# 	if trialF < bestF:
	# 		bestY = trialY
	# 		bestX = trialX
	# 		bestF = trialF
	#----------------------------------------------------------------------

	print()
	print()
	print()

	print("bestX, bestY, bestF: ", round(bestX,2), " ", round(bestY,2), " ", round(bestF,2), " ")
	
	print()
	print()
	print()

main()