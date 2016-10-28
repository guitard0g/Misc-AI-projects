#MACHINE VISION

# color = f.readline()
# print(color)
# f.readline()
# size_x, size_y = f.readline().split()
# print(size_x, size_y)
# maxx = f.readline().splitlines()
# print(maxx)
# pic = f.read().split()
# # print(pic)
# for i in range(0, len(pic)):
# 	pic[i]=float(pic[i])
# for i in range(0, len(pic), 3):
# 	red=pic[i]
# 	green=pic[i+1]
# 	blue=pic[i+2]
# 	gray = 0.30 * red + 0.59 * green + 0.11 * blue
# 	pic[i]=gray
# 	pic[i+1]=gray
# 	pic[i+2]=gray

from tkinter import *
from time import clock
from random import choice
from pickle import dump
from pickle import load
# import Image

root = Tk()
START = clock()
WIDTH = 824
HEIGHT = 582
COLORFLAG = False
HIGH = 45
LOW = 10
class ImageFrame:
	def __init__(self, image, COLORFLAG=False):
		self.img = PhotoImage(width = WIDTH, height=HEIGHT)
		for row in range(HEIGHT):
			for col in range(WIDTH):
				num = image[row*WIDTH + col]
				if COLORFLAG ==True:
					kolor = "#%02x%02x%02x" % (num[0], num[1], num[2])
				else:
					kolor = "#%02x%02x%02x" % (num, num, num)
				self.img.put(kolor, (col, row))
		c = Canvas(root, width = WIDTH, height = HEIGHT); c.pack()
		c.create_image(0,0, image = self.img, anchor = NW)
		printElapsedTime('displayed image')
def printElapsedTime(msg = 'time'):
	length = 30
	msg = msg[:length]
	tab = '.'*(length-len(msg))
	print('--'+msg.upper()+tab+' ', end='')
	time = round(clock()-START, 1)
	print( '%2d'%int(time/60), ' min :', '%4.1f'%round(time%60, 1), \
			' sec', sep = '')
def displayImageInWindow(image):
	global x
	x = ImageFrame(image)

def imageNoise(points, image):
	from random import randint
	for n in range(points):
		r = randint(0, HEIGHT-1)
		c = randint(0, WIDTH-1)
		image[(r*WIDTH)+c] = 255

def drawLine(m, b, image):
	for x in range(WIDTH):

		index = ((m*x+b)*WIDTH+x)
		if 0 <= index < len(image):
			image[index] = 255

def grayScale(file1, pic, image):
	for pos in range(0, len(pic), 3):
		RGB = (int(pic[pos+0]), int(pic[pos+1]), int(pic[pos+2]))
		image.append(int(0.2*RGB[0]+0.7*RGB[1]+0.1*RGB[2]))
	printElapsedTime('Gray numbers are now created')

	for elt in image:
		file1.write(str(elt)+' ')
	printElapsedTime('Saved file numbers')

	return image
def sobel(file1, image):
	for pos in range(image):
		left = grayImage[y*WIDTH+x-1]
		points.append(left*-2)
		right = grayImage[y*WIDTH+x+1]
		points.append(right*2)
		#:(
		upLeft = grayImage[(y-1)*WIDTH+x-1]
		points.append(upLeft)
		upRight = grayImage[(y-1)*WIDTH+x+1]
		points.append(upRight)
		downLeft = grayImage[(y+1)*WIDTH+x-1]
		points.append(downLeft)
		downRight = grayImage[(y+1)*WIDTH+x+1]
		points.append(downRight)
		weightedValue = (1/16)*(sum(points))
		copy[y*WIDTH+x] = weightedValue
def blur(file1, grayImage):
	copy = grayImage[:]
	for pos in range( len(grayImage) ):
		x = pos%WIDTH
		y = pos//WIDTH
		if 0<x<WIDTH-1 and 0<y<HEIGHT-1:
			points = []
			top = grayImage[(y-1)*WIDTH+x]
			points.append(top*2)
			bottom = grayImage[(y+1)*WIDTH+x]
			points.append(bottom*2)
			left = grayImage[y*WIDTH+x-1]
			points.append(left*2)
			right = grayImage[y*WIDTH+x+1]
			points.append(right*2)
			upLeft = grayImage[(y-1)*WIDTH+x-1]
			points.append(upLeft)
			upRight = grayImage[(y-1)*WIDTH+x+1]
			points.append(upRight)
			downLeft = grayImage[(y+1)*WIDTH+x-1]
			points.append(downLeft)
			downRight = grayImage[(y+1)*WIDTH+x+1]
			points.append(downRight)
			points.append(4*grayImage[y*WIDTH+x])
			weightedValue = (1/16)*(sum(points))
			copy[y*WIDTH+x] = weightedValue
	printElapsedTime('Blurred numbers are now created')
	for elt in copy:
		file1.write(str(elt)+' ')
	printElapsedTime('Saved file numbers ( blur() )')

	return copy
def main():
	
	# file1 = open("testPic.ppm")
	# stng = file1.readline()
	# print(stng)
	# stng = file1.readline()
	# print(stng)
	# stng = file1.readline()
	# print(stng)
	# stng = file1.readline()
	# print(stng)
	# pic = file1.read().split()
	# image = []
	# file1.close()
	# file1 = open('grayScale.ppm', 'w')
	# image = grayScale(file1, pic, image)
	# for i in range(10):
	# 	image = blur(file1, image)
	# file1.close()
	# fout = open( 'image.pkl' , 'wb' )
	# #
	# dump( image , fout , protocol = 2 )
	# #
	# fout.close()
#
	image = load( open( 'image.pkl' , 'rb' ) )	
	# for pos in range(0, len(pic), 3):
	# 	RGB = (int(pic[pos+0]), int(pic[pos+1]), int(pic[pos+2]))
	# 	image.append(int(0.2*RGB[0]+0.7*RGB[1]+0.1*RGB[2]))
	# printElapsedTime('Gray numbers are now created')
	# file1 = open('grayScale.ppm', 'w')

	# # print(pic)
	# for elt in image:
	# 	file1.write(str(elt)+' ')
	# printElapsedTime('Saved file numbers')
	# file1.close()
	displayImageInWindow(image)
	root.mainloop()



if __name__ == '__main__':
	main()
		


