from tkinter	import *

root	=	Tk()
WIDTH	=	512
HEIGHT	=	512
HIGH		= 15
LOW			= 5
from math import pi, cos, sin,sqrt, atan2

angleRange	= int(2*pi/0.01)
radiusRange	= int(2*512)
NUMBER_OF_TIMES_TO_SMOOTH_IMAGE = 6

class ImageFrame:
	def __init__(self, colors, wd = WIDTH, ht = HEIGHT, colorFlag = False):
		self.img = PhotoImage(width = wd, height = ht)
		for row in range(ht):
			for col in range(wd):
				num = colors[row*wd + col]
				if num==255 or num < 252:
					kolor = "#%02x%02x%02x" %(int(num), int(num), int(num))
				if num == 254:
					kolor = "#%02x%02x%02x" %(int(num), 0, 0)
				if num == 253:
					kolor = "#%02x%02x%02x" %(0, int(num), 0)
				if num == 252:
					kolor = "#%02x%02x%02x" %(0, 0, int(num))
				if not (0<=num<256):
					exit('ERROR: num = ' + num)
				self.img.put(kolor, (col,row))
		c = Canvas(root, width = wd, height = ht); c.pack()
		c.create_image(0,0, image = self.img, anchor = NW)

def frange(start, stop, step):
    i = start
    terminate = stop-(step/10)
    while i<terminate:
        yield i
        i += step

def drawCircleOutline(r,cx,cy,image):
    for t in frange(0,2*pi,0.001):
        xi=int(cx+r*cos(t))
        yi=int(cy+r*sin(t))
        image[WIDTH*xi+yi]=255
    return image

def drawCircle(r,cx,cy,image):
	for x in range(HEIGHT):
		for y in range(WIDTH):
			if (x-cx)**2+(y-cy)**2 <= r**2:
				image[WIDTH*x+y]=225
	return image

def drawRedCircle(x, y, r, image, start = 0, stop = 512):
	for x in range(start, stop):
		y=x*m+b
		image[int(y)*WIDTH+x]=[255,0,0]
	return image

def saveStructureDataToFIle(imageLists, fileName):
	import pickle
	file1 = open(fileName, 'wb')
	pickle.dump(imageLists, file1)
	file1.close()

def extractStructuredDataFromFile(fileName):
	import pickle
	file1 = open(fileName, "rb")
	imageLists = pickle.load(file1)
	file1.close()
	return imageLists

def drawMBLine(m, b, image, start = 0, stop = WIDTH):
	step = 1
	if stop-start<0: step=-1
	for x in range(start,stop,step):
		y=round(m*x + b, 0)*WIDTH
		if 0 <= (y+x) < (WIDTH*HEIGHT):
			image[int(y+x)] = 255
	return image


#--------------------------Image Smoothing----------------------------------------

def extractTheImageGrayScaleNumbersFromFile(GRAY_SCALE_NUMBERS_FILE_NAME = 'circle.ppm'):
    file1 = open(GRAY_SCALE_NUMBERS_FILE_NAME,'r')
    nums = file1.read()
    nums = nums.split('')
    file1.close()
    image = []
    for elt in nums[3:]:
        image.append(int(elt))
    return image

def extractSmoothAndSaveImage(IMAGE_FILE_NAME = 'circle.ppm'):
	image = list(extractStructuredDataFromFile (IMAGE_FILE_NAME))
	blurr=blurrImage(image)
	saveStructureDataToFIle(blurr, 'circsmoothedImage.ppm')
	return 'circsmoothedImage.ppm'

def blurrImage(image):
    mask=[[1,2,1],[2,4,2],[1,2,1]]
    for q in range(NUMBER_OF_TIMES_TO_SMOOTH_IMAGE):
        image2 = [0] *WIDTH *HEIGHT
        for row in range (1, HEIGHT-2):
            for col in range (1, WIDTH-2):
                a=image[(row-1)*WIDTH + col-1]
                b=image[(row-1)*WIDTH + col]
                c=image[(row-1)*WIDTH + col+1]
                d=image[row*WIDTH + col-1]
                e=image[row*WIDTH + col]
                f=image[row*WIDTH + col+1]
                g=image[(row+1)*WIDTH + col-1]
                h=image[(row+1)*WIDTH + col]
                i=image[(row+1)*WIDTH + col+1]
                grid=[[a,b,c],[d,e,f],[g,h,i]]
                image2[row*WIDTH + col] = applymask(grid, mask)
        image=image2
    return image

def applymask(grid, mask):
	gridsum=0
	for r in range(3):
		for c in range(3):
			gridsum=gridsum+(grid[r][c]*mask[r][c])
	return round(gridsum/16)

def sobelTransformOfSmoothedImage(IMAGE_FILE_NAME = 'circsmoothedImage.ppm'):
    image = list(extractStructuredDataFromFile (IMAGE_FILE_NAME))
    nimage = sobelImage(image)
    return nimage

def sobelImage(image):
    Sy=[[1,2,1],[0,0,0],[-1,-2,-1]]
    Sx=[[-1,0,1],[-2,0,2],[-1,0,1]]
    image2=[[0,0,0,0,0] for a in range(HEIGHT*WIDTH)]
    for row in range (1, HEIGHT-1):
        for col in range (1, WIDTH-1):
            grid=[[image[(row-1)*WIDTH + col-1],image[(row-1)*WIDTH + col],image[(row-1)*WIDTH + col+1]],[image[row*WIDTH + col-1],image[row*WIDTH + col],image[row*WIDTH + col+1]],[image[(row+1)*WIDTH + col-1],image[(row+1)*WIDTH + col],image[(row+1)*WIDTH + col+1]]]
            Gx, Gy = SobelTransform(Sy, Sx, grid)
            image2[row*WIDTH + col] = [sqrt(Gx*Gx + Gy*Gy), theta(Gx, Gy), 0, 0, 0]
    return image2

def SobelTransform(Sy, Sx, grid):
    Gx=0
    Gy=0
    for r in range(3):
        for c in range(3):
            Gx=Gx+(grid[r][c]*Sx[r][c])
            Gy=Gy+(grid[r][c]*Sy[r][c])
    return round(Gx/16), round(Gy/16)

def theta(Gx, Gy):
    angle=atan2(Gy, Gx) + pi*(Gy<0)
    return round((angle%(7*pi/8))*4/pi)

def normalize(image, intensity = 225):
    m = max(image)
    printElapsedTime('normalizing')
    return [int(x*intensity/m) for x in image]

def cannyTransform (M):
    for row in range (1, HEIGHT-1):
        for col in range (1, WIDTH-1):
            fillCellAt(M, row, col)
    return M

def fillCellAt(M, row, col):
    if M[row*WIDTH + col][3]== 1: return
    M[row*WIDTH + col][3] = 1
    if not checkEdgePoint(M, row, col):return
    M[row*WIDTH + col][2]=1
    if (row > 0  and M[(row-1)*WIDTH + col][0] > LOW):
        M[(row-1)*WIDTH + col][4]=1
        fillCellAt(M, row-1, col)
    if (col > 0  and M[row*WIDTH + col-1][0] > LOW):
        M[row*WIDTH + col-1][4]=1
        fillCellAt(M, row, col-1)
    if (row < WIDTH-1  and M[(row+1)*WIDTH + col][0] > LOW):
        M[(row+1)*WIDTH + col][4]=1
        fillCellAt(M, row+1, col)
    if (col < HEIGHT-1  and M[row*WIDTH + col+1][0] > LOW):
        M[row*WIDTH + col+1][4]=1
        fillCellAt(M, row, col+1)
    if M[row*WIDTH + col][0]< HIGH: return
    M[row*WIDTH + col][4]=1
    fillCellAt(M, row-1, col)
    fillCellAt(M, row+1, col)
    fillCellAt(M, row, col-1)
    fillCellAt(M, row, col+1)


def checkEdgePoint(M, r, c):
    if M[r*WIDTH + c][1]==0: return (M[r*WIDTH + c-1][0]<M[r*WIDTH + c][0]) and (M[r*WIDTH + c+1][0]<M[r*WIDTH + c][0])
    if M[r*WIDTH + c][1]==1: return (M[(r-1)*WIDTH + c+1][0]<M[r*WIDTH + c][0]) and (M[(r+1)*WIDTH + c-1][0]<M[r*WIDTH + c][0])
    if M[r*WIDTH + c][1]==2: return (M[(r-1)*WIDTH + c][0]<M[r*WIDTH + c][0]) and (M[(r+1)*WIDTH + c][0]<M[r*WIDTH + c][0])
    if M[r*WIDTH + c][1]==3: return (M[(r-1)*WIDTH + c-1][0]<M[r*WIDTH + c][0]) and (M[(r+1)*WIDTH + c+1][0]<M[r*WIDTH + c][0])

def doubleThreshholdImageListsInToGrayScaleValues(cannyImageLists):
    imageofEdges = [0 for i in range(WIDTH*HEIGHT)]
    for x in range(WIDTH*HEIGHT):
        if cannyImageLists[x][4]==1: imageofEdges[x]=255
    return imageofEdges

#----------------------------Image smoothing ends---------------------


def main():
    image=[0 for elt in range(HEIGHT * WIDTH)]

    image=drawCircle(100,250,250,image)
    imageFileName='circle.ppm'
    saveStructureDataToFIle(image, imageFileName)

    smoothedFileName = extractSmoothAndSaveImage (imageFileName)
    sobelImageList	= sobelTransformOfSmoothedImage (smoothedFileName)
    cannyImageLists		= cannyTransform (sobelImageList)
    finalImageofEdges	= doubleThreshholdImageListsInToGrayScaleValues (cannyImageLists)



    x = ImageFrame(image)
    root.mainloop()
if __name__ == "__main__": main()
