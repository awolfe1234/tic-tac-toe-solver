import random
import sys
import copy
sys.setrecursionlimit(16000)
solutions = []
maxsol = 5
solfound = 0

class Board:
	def __init__(self, n):
		self.n = n
		self.board = []
		self.empty = []
	# take second element for sort
	def takeSecond(self, elem):
	    return elem[1]

	def addrow(self,val):
		row = []
		for x in val:
			row.append(int(x))
		self.board.append(row)

	def weighted(self, x, y):
		sm = 0
		for i in range(0, self.n):
			if(self.board[i][y] != 0):
				sm += 1 
		for j in range(0, self.n):
			if(self.board[x][j] != 0):
				sm += 1
		return sm

	#updates the empty space list 
	def findEmpty(self):

		self.empty.clear()
		for x in range(0,self.n):
			for y in range(0,self.n):
				if(self.board[x][y] == 0):
					self.empty.append(((x,y),self.weighted(x,y)))
		
		self.empty.sort(key=self.takeSecond, reverse=True)	
		

	#Prints 1 and 2 version 	
	def printboard(self):
		for x in range(0,self.n):
			for y in range(0,self.n):
				print(self.board[x][y],end=' ')
			print()

	#Prints X and O version 
	def printboard2(self):
		for x in range(0,self.n):
			print(' ',end = '')
			for y in range(0,self.n):
				if(self.board[x][y] == 1):
					print('X',end=' ')
				elif(self.board[x][y] == 2):
					print('O',end=' ')
				elif(self.board[x][y] == 0):
					print(' ',end= ' ')
			print()

#Checks to ensure all params were followed when solving 
def finalcheck(b):
	#check for rows/cols of three 
	for x in range(0, b.n):
		for y in range(0, b.n):
			if(y <= b.n-3 and b.board[x][y] == b.board[x][y+1] and b.board[x][y] == b.board[x][y+2]):
				return False
			if(y <= b.n - 3 and b.board[y][x] == b.board[y+1][x] and b.board[y][x] == b.board[y+2][x]):
				return False







	#check for even row/col totals 
	for i in range(0, b.n):

		if(totals(1, b.board[i]) != (b.n/2)):
			return False 

		if(totals(2, b.board[i]) != (b.n/2)):
			return False 	
			
		col = colCreator(b,i)

		if(totals(1, col) != (b.n/2)):
			
			return False 

		if(totals(2, col) != (b.n/2)):
			
			return False 

	#check to ensure no 2 rows are the same 
	for x in range(0, b.n-1):
		row = b.board[x]
		for x2 in range(x+1, b.n):
			if(row== b.board[x2]):

				return False 

	#check to make sure no 2 cols are the same 
	for x in range(0, b.n-1):
		col = colCreator(b, x)
		for y in range(x+1, b.n):
			col2 = colCreator(b, y)
			if(col == col2):
				return False 

	return True 

#Not a solve check, checks to ensure the board is full, returns a bool 
def boardFull(b):
	for i in range(0,b.n):
		for j in range(0,b.n):
			if(b.board[i][j] == 0):
				return False
	return True 

#Checks if a given list contains a 0 
def isFull(row):
	for x in row:
		if(x == 0):
			return False
	return True 

#Creates a board from the input file 
def createBoard(inputFile):
	f = open(inputFile,"r")
	lines = f.readlines()
	b = Board(int(lines[0].rstrip("\n"))) 
	for x in lines[1:]:
		b.addrow(x.rstrip("\n"))
	b.findEmpty()
	#print(b.empty)
	return b

#Adds a solution to a solution holder, ensures duplicates are ignored 
def addSolution(b):
	global solutions 
	if(b not in solutions):
		global solfound 

		solfound +=1
		print("\n Solution:")
		b.printboard2()
		solutions.append(b)

#Main solving function 
def solve(B, i, j, v):
	if(end() == True):
		return 
	holdb = copy.deepcopy(B)
	holdb.board[i][j] = v
	BP = propagate(holdb)
	if(finalcheck(BP) == False and boardFull(BP) == True):
		return 
	else:
		if(finalcheck(BP) == True):
			addSolution(BP)
			#BP.printboard2()
			return 
		else:
			BP.findEmpty()
			#newVals = random.choice(BP.empty)
			if(len(BP.empty) > 0):
				newVals = BP.empty[0]
				solve(BP,newVals[0][0],newVals[0][1],2)
				solve(BP,newVals[0][0],newVals[0][1],1)


#forces all branches to close after min number of solutions is found 
def end():
	if(maxsol == solfound):
		return True 
	else:
		return False


#Countes the empty cells of a given row (returns total ammount of empty spaces and the last spot at which one occured)
def totalEmpty(row):
	count = 0
	spot = 0
	spot_count = -1
	for x in row:
		spot_count += 1
		if (x == 0):
			count += 1
			spot = spot_count 
	return (count,spot) 

def totals(toCount, lst):
	count = 0
	for x in lst:
		if(x == toCount):
			count +=1
	return count 

#  full not full                 True if the two are similar execpt for two spaces 
#takes two rows, returns a tuple (Bool, [pos1, pos2])
def compare(f1,r2):
	spots = []
	spot = 0
	for x,y in zip(f1,r2):
		spot +=1
		if(x != y):
			spots.append(spot)
	if(len(spots) == 2):
		return (True, spots)
	else:
		return (False,spots)

def colCreator(b,index):
	newCol = []
	for i in range(0,b.n):
		newCol.append(b.board[i][index])
	return newCol

def propagate(b):
	while(True):
		brk = 0
		#Constraint 1
		for i in range(0, b.n):
			for j in range(0, b.n):
				tempRow = []
				if(j <= b.n-3):
					tempRow.append(b.board[i][j])
					tempRow.append(b.board[i][j+1])
					tempRow.append(b.board[i][j+2])
					empty = totalEmpty(tempRow)
					if(empty[0] == 1):
						#if the sum is 2 then we have two 1's meaning the 0 should be a 2
						if(b.board[i][j] + b.board[i][j+1] + b.board[i][j+2] == 2):
							b.board[i][j+empty[1]] = 2
							brk = 1
						elif(b.board[i][j] + b.board[i][j+1] + b.board[i][j+2] == 4):
							b.board[i][j+empty[1]] = 1
							brk = 1
					tempRow.clear()
				if(i <= b.n-3):
					tempRow.append(b.board[i][j])
					tempRow.append(b.board[i+1][j])
					tempRow.append(b.board[i+2][j])
					empty2 = totalEmpty(tempRow)
					if(empty2[0] == 1):
						#if the sum is 2 then we have two 1's meaning the 0 should be a 2
						if(b.board[i][j] + b.board[i+1][j] + b.board[i+2][j] == 2):
							b.board[i+empty2[1]][j] = 2
							brk = 1
						elif(b.board[i][j] + b.board[i+1][j] + b.board[i+2][j] == 4):
							b.board[i+empty2[1]][j] = 1
							brk = 1
					tempRow.clear()
		#Constraint 2 
		for i in range(0, b.n):
			if(totals(1, b.board[i]) == (b.n/2)):
				for a in range(0, b.n):
					if(b.board[i][a] == 0):
						b.board[i][a] = 2
						brk = 1
			if(totals(2, b.board[i]) == (b.n/2)):
				for a in range(0, b.n):
					if(b.board[i][a] == 0):
						b.board[i][a] = 1
						brk = 1

		
			col = colCreator(b,i)

			if(totals(1, col) == (b.n/2)):

				for a in range(0, b.n):
					if(b.board[a][i] == 0):
						b.board[a][i] = 2
						brk = 1
			if(totals(2, col) == (b.n/2)):
				for a in range(0, b.n):
					if(b.board[a][i] == 0):
						b.board[a][i] = 1
						brk = 1

		#Constraing 3
		#Row
		for i in range(0, b.n):
			row1 = b.board[i]
			if(isFull(row1)):
				for j in range(0, b.n):
					if(i != j and totals(0,b.board[j]) == 2):
						test = compare(row1,b.board[j])
						if(test[0] == True):
							b.board[j][test[1][0]-1] = row1[test[1][1]-1]
							b.board[j][test[1][1]-1] = row1[test[1][0]-1]
							brk = 1

		#Col					
		for i in range(0, b.n):
			col1 = colCreator(b,i)

			if(isFull(col1)):
				for j in range(0, b.n):
					if(i != j):
						col2 = colCreator(b,j)
						if(totals(0,col2) == 2):
							test = compare(col1,col2)
							if(test[0] == True):
								b.board[test[1][0]-1][j] = col1[test[1][1]-1]
								b.board[test[1][1]-1][j] = col1[test[1][0]-1]
								brk = 1
		if(brk == 0):
			break
	b.findEmpty()
	return b


b = createBoard("Puzles/10x10hard.txt")
print("Starting board")
b.printboard2()
newVals = b.empty[0]
solve(copy.deepcopy(b),newVals[0][0],newVals[0][1],2)
solve(copy.deepcopy(b),newVals[0][0],newVals[0][1],1)

	








