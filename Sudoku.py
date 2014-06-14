#=================================
#Name: Shijing Liu
#Homework 3 Question 2 Question 4 Question 6 
#=================================

import copy

#=========================
#define cross function for creation of column, row and blocks
#==========================
def cross (A, B):
    return [a+b for a in A for b in B]


#=========================
#define sudoku class 
#==========================
class sudoku():
	def __init__(self, filename):
		f = open(filename, "r")
		digits = '123456789'
		rows = digits
		cols = digits
		squares = cross (rows, cols)
		unitlist = ([cross(rows, c) for c in cols] + [cross (r, cols) for r in rows] + [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
		units = dict((s, [u for u in unitlist if s in u]) for s in squares)
		peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)

		self.domain = {}
		count = 0
		for line in f:
			for char in line:
				if char == "*":
					self.domain[count] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
					count += 1
				else:
					if not char == "\n":
						self.domain[count] = [int(char)]
						count += 1

#=========================
#create arc constraints 
#==========================

		self.constraints = []
		for i in range(0, len(squares)):
			 a1 = int(squares[i][0])
			 a2 = int(squares[i][1])
			 currentNum = (a1-1)*9 + a2-1
			 currentPeer = peers [squares[i]]
			 while not currentPeer == set():
					peerEle = currentPeer.pop()
					p1 = int(peerEle[0])
					p2 = int(peerEle[1])
					thisPeer = (p1-1)*9+p2-1
					if not (currentNum, thisPeer, "cons") in self.constraints:
						self.constraints.append((currentNum, thisPeer, "cons"))

            
                        
                        
                        
		for i in range(0, 9):
			for j in xrange(9*i, 9*i + 9):
				for k in xrange(9*i, 9*i + 9):
					if not j == k and not (j, k, "r") in self.constraints:
						self.constraints.append((j, k, "r"))
		for i in range(0, 9):
			for j in range(0, 9):
				for k in xrange(9*i + j, 81, 9):
					for l in xrange(9*i + j, 81, 9):
						if not k == l and not (k, l, "c") in self.constraints:
							self.constraints.append((k, l, "c"))
 
		block = [0, 3, 6, 27, 30, 33, 54, 57, 60]
		for num in block:
			for i in xrange(3):
				for j in xrange(3):
					for k in xrange(3):
						for l in xrange(3):
							if not i + 9*j == k + 9*l and not (i + 9*j + num, k + 9*l + num, "b") in self.constraints:
								self.constraints.append((i + 9*j + num, k + 9*l + num, "b"))
		f.close()

#==============================
#the AC-3 algorithm, Question 2 
#==============================
	def getAC_3(self, domain):
		queue = []
		for constraint in self.constraints:
			queue.append(constraint)

		while queue:
			(xi, xj, cons) = queue.pop(0)
			if self.AC_3_helper(xi, xj, domain):
				for (a, b, c) in self.constraints:
					if b == xi and not a == xj:
						queue.append((a, b, c))
			if not domain[xi]:
				return 0

		for key in domain:
			if not len(domain[key]) == 1:
				return 1
		return 2


	def AC_3_helper(self, a, b, domain):
		if len(domain[b]) == 1 and domain[b][0] in domain[a]:
			domain[a].remove(domain[b][0])
			return True
		return False



	    
	def ac3_solution(self):
		if self.getAC_3(self.domain) == 2:
			stri = ""
			count = 0
			for key in self.domain:
				stri += str(self.domain[key][0])
				count += 1
				if count == 9:
					count = 0
					stri += "\n"
			print stri
		else:
			print "No solution"




#============================================
#the backtracking search that calls AC-3 algorithm
#as a subroutine. This Solves both Question 4 and
#Question 6
#============================================
	def strategy2(self):
		temp = copy.deepcopy(self.domain)
		for i in xrange(81):
			row = [i]
			col = [i]
			block = [i]
			for (a, b, c) in self.constraints:
				if a == i:
					if c == "r":
						row.append(b)
					elif c == "c":
						col.append(b)
					else:
						block.append(b)

			d1 = {}
			for var in row:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d1:
							d1[val] = [var]
						else:
							d1[val].append(var)

			for key in d1:
				if len(d1[key]) == 1:
					temp[d1[key][0]] = [key]
			self.getAC_3(temp)

			d2 = {}
			for var in col:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d2:
							d2[val] = [var]
						else:
							d2[val].append(var)

			for key in d2:
				if len(d2[key]) == 1:
					temp[d2[key][0]] = [key]
			self.getAC_3(temp)

			d3 = {}
			for var in block:
				if len(temp[var]) > 1:
					for val in temp[var]:
						if not val in d3:
							d3[val] = [var]
						else:
							d3[val].append(var)

			for key in d3:
				if len(d3[key]) == 1:
					temp[d3[key][0]] = [key]
			self.getAC_3(temp)
		self.domain = copy.deepcopy(temp)


	def backtrack(self):
		self.strategy2()
		if self.getAC_3(self.domain) == 2:
			return 2

		temp = copy.deepcopy(self.domain)
		temp2 = copy.deepcopy(self.domain)

		for var in temp2:
			if len(temp2[var]) > 1:
				t = []
				for val in temp2[var]:
					t.append(val)
				for val in t:
					temp2[var] = [val]
					result = self.getAC_3(temp2)
					if result == 2:
						self.domain = copy.deepcopy(temp2)
						return 2
					else:
						temp2 = copy.deepcopy(temp)
		return 0


	def backtrack_solution(self):
		if self.backtrack() == 2:
			stri = ""
			count = 0
			for key in self.domain:
				stri += str(self.domain[key][0])
				count += 1
				if count == 9:
					count = 0
					stri += "\n"
			print stri
		else:
			print "No solution"
			print ""



print "Question 2: ac3 algorithm for ac3solvable:"
sudoku("ac3solvable_example").ac3_solution()
print "Question 2: ac3 algorithm for dp_puzzle:"
sudoku("dp_puzzle").ac3_solution()
print "Question 4: ac3 subroutine algorithm for dp_puzzle:"
sudoku("dp_puzzle").backtrack_solution()
print "Question 4: ac3 subroutine algorithm for gentle sudoku:"
sudoku("gentle_sudoku").backtrack_solution()
print "Question 4: ac3 subroutine algorithm for moderate sudoku:"
sudoku("moderate_sudoku").backtrack_solution()
print "Question 6: backtrack algorithm for diabolical sudoku:"
sudoku("diabolical_sudoku").backtrack_solution()
print "Question 6: backtrack algorithm for guessing sudoku:"
sudoku("guessing_puzzle").backtrack_solution()
