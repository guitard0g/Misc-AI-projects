class ImageFrame:
    def __init__(self, pixels):
        self.img = PhotoImage(width = WIDTH, height = HEIGHT)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                num = pixels[row*WIDTH + col]
                if num=='g':
                    num='g'
                if COLORFLAG == True:
                    kolor = "#%02x%02x%02x" %(num[0], num[1], num[2])
                else:
                    kolor = "#%02x%02x%02x" %(int(num), int(num), int(num))
                self.img.put(kolor, (col,row))
        c = Canvas(root, width = WIDTH, height = HEIGHT); c.pack()
        c.create_image(0,0, image = self.img, anchor = NW)
        printElapsedTime('displayed image')

def printElapsedTime(msg = 'time'):
    length =30
    msg = msg[:length]
    tab = '.'*(length-len(msg))
    print('--' + msg.upper() + tab + ' ', end = '')
    time = round(clock() - START, 1)
    print( '%2d'%int(time/60), ' min :','%4.1f'%round(time%60,1), ' sec', sep = '')

def displayImageInWindow(image):
    global x
    x = ImageFrame(image)

def confirmP3fileType(file1):
	stng = file1.readline().strip()
	if stng[0]+stng[1] != 'P3':
		print('+===================================================+')
		print('| ERROR: This file in NOT of type P3                |')
		print('|        The first line of the file is shown below. |')
		print('+===================================================+')
		print('-->', stng)
		file1.close()
		exit()

def readFileNumbersIntoString(file1):
	nums = file1.read().split()
	file1.close()
	if len(nums)%3 != 0:
		print('---WARNING: Size of file(', len(nums) ,') % 3 !=0')
		exit()
	return nums

def convertStringRGBsToGrayIntegersOrColorTuples(nums):
    COLORFLAG=False
    image = []
    r=0
    g=0
    b=0
    for i in range(len(nums)//3):
        r=int(nums[3*i])
        g=int(nums[3*i+1])
        b=int(nums[3*i+2])
        image.append(int(0.30*r+0.59*g+0.11*b))
    return image



def printTitleAndSizeOfImageInPixels(image):
	print('         ==<RUN TIME INFORMATION>==')
	if len(image)-1 != WIDTH * HEIGHT:
		print('--ERROR: Stated file size not equal to number of pixels')
		print('file length:', len(image))
		print('width:', WIDTH, 'height:', HEIGHT)
		exit()
	print('--NUMBER OF PIXELS............. ', len(image)-1)
	printElapsedTime('image extracted from file')

def readPixelColorsFromImageFile(IMAGE_FILE_NAME):
	imageFile	= open(IMAGE_FILE_NAME,  'r', encoding="utf8")
	confirmP3fileType(imageFile)
	nums = readFileNumbersIntoString(imageFile)
	image = convertStringRGBsToGrayIntegersOrColorTuples(nums)
	printTitleAndSizeOfImageInPixels(image)
	return image

def extractTheImageGrayScaleNumbersFromFile(GRAY_SCALE_NUMBERS_FILE_NAME = 'grayScale.ppm'):
    file1 = open(GRAY_SCALE_NUMBERS_FILE_NAME,'r')
    nums = file1.read().split()
    file1.close()
    image = []
    for elt in nums[3:]:
        image.append(int(elt))
    printElapsedTime ('Extracted gray-scale nums from file')
    return image

def convertColorFileToGrayScaleFile(IMAGE_FILE_NAME = 'lenna.ppm'):
    image = list(readPixelColorsFromImageFile (IMAGE_FILE_NAME))
    saveImageNumbersToFile(image, 'grayScale.ppm')
    return 'grayScale.ppm'

def saveImageNumbersToFile(image, name):
    gray = open(name,'w')
    gray.write('P3')
    gray.write('\n512 512')
    gray.write('\n255')
    for i in range(len(image)):
        gray.write(' '+str(image[i]))

def extractSmoothAndSaveImage(IMAGE_FILE_NAME = 'grayScale.ppm'):
	image = list(extractTheImageGrayScaleNumbersFromFile (IMAGE_FILE_NAME))
	blurr=blurrImage(image)
	saveImageNumbersToFile(blurr, 'smoothedImage.ppm')
	return 'smoothedImage.ppm'

def blurrImage(image):
	mask=[[1,2,1],[2,4,2],[1,2,1]]
	for q in range(NUMBER_OF_TIMES_TO_SMOOTH_IMAGE):
		image2 = [0] *WIDTH *HEIGHT
		for row in range (1, HEIGHT-1):
			for col in range (1, WIDTH-1):
				grid=[[image[(row-1)*WIDTH + col-1],image[(row-1)*WIDTH + col],image[(row-1)*WIDTH + col+1]],[image[row*WIDTH + col-1],image[row*WIDTH + col],image[row*WIDTH + col+1]],[image[(row+1)*WIDTH + col-1],image[(row+1)*WIDTH + col],image[(row+1)*WIDTH + col+1]]]
				image2[row*WIDTH + col] = applymask(grid, mask)
		image=image2
	return image

def applymask(grid, mask):
	gridsum=0
	for r in range(3):
		for c in range(3):
			gridsum=gridsum+(grid[r][c]*mask[r][c])
	return round(gridsum/16)

def sobelTransformOfSmoothedImage(IMAGE_FILE_NAME = 'smoothedImage.ppm'):
    image = list(extractTheImageGrayScaleNumbersFromFile (IMAGE_FILE_NAME))
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

from tkinter	import *
from time		import clock
from sys		import setrecursionlimit
from math       import sqrt
from math       import atan2
from math       import pi
setrecursionlimit(7000)

root		=Tk()
START		=clock()
WIDTH		= 512
HEIGHT		= 512
COLORFLAG	= False
HIGH		= 10
LOW			= 5
NUMBER_OF_TIMES_TO_SMOOTH_IMAGE = 6

def main():
    imageFileName = 'lenna.ppm'

    grayScaleNumbersFileName = convertColorFileToGrayScaleFile (imageFileName)
#    image = list(readPixelColorsFromImageFile(imageFileName))
#    displayImageInWindow(image)

    smoothedFileName = extractSmoothAndSaveImage (grayScaleNumbersFileName)
#    image = extractTheImageGrayScaleNumbersFromFile(smoothedFileName)
#    displayImageInWindow(image)

    sobelImageList	= sobelTransformOfSmoothedImage (smoothedFileName)
#    mags = normalize([x[0] for x in sobelImageList])
#    x = ImageFrame(mags)

    cannyImageLists		= cannyTransform (sobelImageList)
    finalImageofEdges	= doubleThreshholdImageListsInToGrayScaleValues (cannyImageLists)
    displayImageInWindow(finalImageofEdges)
    root.mainloop()

if __name__=='__main__': main()
