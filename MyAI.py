# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

# My suggestions on how to do this:
# 	Make a 2d array of custom data structures, where each structure has the current state of the node it represents and
# 	pointers to the nodes adjacent to it. By default, all nodes are unknown (covered) except for that first given node.
#
# 	There should also be a list containing pointers to all the nodes on the "frontier"; that is to say, to all
# 	unrevealed nodes adjacent to a revealed node. These are the nodes to be acted on first. One thing to mention is that
# 	we should make it so nodes that become flagged are removed from this list, and put into a seperate one. The flagged
# 	nodes list should be modified as we add flagged nodes and remove flags from nodes.
#
# 	Whenever a numbered node is encountered, immediately flag all covered adjacent nodes. This way can uncover as much
# 	of the board as possible in complete safety before we have to start taking chances on flagged nodes. Of course, the
# 	process of mapping the rest of the board should also allow us to remove flags from nodes in the process, shrinking
# 	this list and increasing the size of the frontier list.
#

from AI import AI
from Action import Action

#each node in array is either:
#	-2: bomb
#	-1: covered
#	 0: uncovered, no adjacent bomb
#  #>0: # of adjacent bombs


#condition to win is when frontier is empty and minefield has the same number of element in it as there are bombs.
#uncover every square that is not a bomb.

class MyAI( AI ):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        self.X = startX
        self.Y = startY
        self.board = [[-1 for i in range(rowDimension)] for j in range(colDimension)]
        self.move = 0
        self.uncovered = []
        self.uncoveredOnes = []
        self.frontier = []
        self.minefield = []



	#pulls from either frontier or (if frontier is empty) minefield
	#uncovers that tile, and then adds adjacent covered tiles (that are not already in frontier or minefield) into them
	#	as appropriate
	#modifies the data for the tile in the 2d array
	def getAction(self, number: int) -> "Action Object":

        if self.move == 0:
            tile = self.startX * 10 + self.startY
            self.uncovered.append(tile)
            self.board[self.startX][self.startY] = number;
        else:
            self.board[Y][X] = number;
            if number > 0:
                tile = self.X * 10 + self.Y
                self.uncoveredOnes.append(tile)

        if number==0:
		    addQueue(0, self.X, self.Y)
		elif number > 0:
			addQueue(1, self.X, self.Y)

        if self.frontier not empty:
            tile = self.frontier.pop()
            self.X = tile//10
            self.Y = tile%10
            self.uncovered.append(tile)
            self.move += 1
            return Action(AI.Action.UNCOVER, self.X, self.Y)
        else:
            if len(self.minefield)>self.minefield:
                tile = minMinefield()
                #tile = self.minefield.pop()
                self.X = tile//10
                self.Y = tile%10
                self.uncovered.append(tile)
                self.move += 1
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

    # b = 0 => frontier and b = 1 => minefield
	def addQueue(self, int, b: int, X: int, Y: int):

		# add top left
		if !outOfBound(self.X-1, self.Y+1):
			tile = (self.X - 1) * 10 + (self.Y + 1)
            if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add middle left
		if !outOfBound(self.X-1, self.Y):
			tile = (self.X - 1) * 10 + (self.Y)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add bottom left
		if !outOfBound(self.X-1, self.Y-1):
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add center top
		if !outOfBound(self.X, self.Y+1):
			tile = (self.X) * 10 + (self.Y + 1)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add center bottom
		if !outOfBound(self.X, self.Y-1):
			tile = (self.X) * 10 + (self.Y - 1)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add top right
		if !outOfBound(self.X+1, self.Y+1):
			tile = (self.X + 1) * 10 + (self.Y + 1)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add middle right
		if !outOfBound(self.X+1, self.Y):
			tile = (self.X + 1) * 10 + (self.Y)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)

		# add bottom right
		if !outOfBound(self.X+1, self.Y-1):
			tile = (self.X + 1) * 10 + (self.Y - 1)
			if b == 0:
                if tile in self.minefield:
                    self.minefield.remove(tile)
                if tile not in self.frontier:
                    self.frontier.append(tile)
            if b == 1:
                if tile not in self.frontier:
                    if tile not in self.minefield:
                        self.minefield.append(tile)


	def outOfBound(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.colDimension or y < 0 or y >= self.rowDimension:
            return True
        return False

    def minMinefield(self)->int:
        minOnes = 9
        minItem = NULL
        for item in self.minefield:
            if numOnes(item) < minOnes
                minOnes = numOnes(item)
                minItem = item
        self.minefield.remove(minItem)
        return minItem

    def numOnes(self, item->int)->int:
        counter = 0
        tileX = item//10
        tileY = item%10

        for ones in self.uncoveredOnes
            onesTileX = ones // 10
            onesTileY = ones % 10

            thisX = tileX - onesTileX
            thisY = tileY - onesTileY

            if -1<=thisX<=1 and -1<=thisY<=1:
                counter += 1

        return counter
