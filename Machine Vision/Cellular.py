from tkinter import *

def setUpCanvas(root):
	root.title("Wolfram's cellular automata: A Tk/Python Graphics Program")
	canvas = Canvas(root, width = 1270, height = 780, bg = 'black')
	canvas.pack(expand = YES, fill = BOTH)
	return canvas

def printList(rule):
	#1. print title
    canvas.create_text(170, 20, text = "Rule " + str(rule), fill = 'gold', font = ('Helvetica', 20, 'bold'))

	#2. set up list and print top row
    L = [1,]
    canvas.create_text(650, 10, text =chr(9607), fill = 'RED', font = ('Helvetica', FSIZE, 'bold'))
	#3. write the rest
    for row in range(90):
        L = ['0','0']+L+['0','0']
        num = []
        for n in range(len(L)-2):
            num.append(int(str(L[n])+str(L[n+1])+str(L[n+2]),2))
        L = []
        for a in num:
            L += str(rule[a])
        kolor = 'RED'
        c=0
        for n in L:
            if n == '0':
                kolor = 'BLACK'
            canvas.create_text(650-row*FSIZE + FSIZE*c, 10+row*FSIZE, text =chr(9607), fill = kolor, font = ('Helvetica', FSIZE, 'bold'))
            c += 1
            kolor = 'RED'

root = Tk()
canvas = setUpCanvas(root)
FSIZE = 8

def main():
    rule = [0,1,0,1,1,0,1,0,]
    # rule = [1,0,1,1,0,1,0,1,]
#	rule = [0,1,1,0,1,1,1,0,]
#	rule = [1,1,0,0,1,1,1,0,]
#	rule = [1,1,1,1,1,1,1,1,]
    printList(rule)
    root.mainloop()

if __name__ == '__main__':
	main()

