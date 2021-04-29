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

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        self.X = startX
        self.Y = startY
        self.board = [[-1 for i in range(rowDimension)] for j in range(colDimension)]
        self.move = 0
        self.frontier = []
        self.minefield = []
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	#pulls from either frontier or (if frontier is empty) minefield
	#uncovers that tile, and then adds adjacent covered tiles (that are not already in frontier or minefield) into them
	#	as appropriate
	#modifies the data for the tile in the 2d array
	def getAction(self, number: int) -> "Action Object":

		int tile;
        int tilex;
        int tiley;

		#if move is 0 (if it is the first move) add the starting uncovered square to the board and add all of its
		#adjacent squares to either frontier or minefield as appropriate.
        if self.move is 0:
            self.board[startY][startX] = number
        else #no need for else since the above is only conditional on it being the first move
            self.board[Y][X] = number

		#now, pull something out of frontier (if it is not empty) or minefield (if frontier is empty).
		#if it pulls out of minefield, we will need to pull out the item with the smallest reference counter (the
		#item in minefield with the smallest number of numbered adjacent squares.
		#Uncover that square (both in the game and self.board), and add all of that square's adjacent covered squares
		#into either frontier or minefield as appropriate.
        if self.board[Y][X].number is 0:
            #add left

            #if self.X>0:
            tile =
            
            #if
        return Action(AI.Action.UNCOVER, startX, st)

		return Action(AI.Action.LEAVE)
  
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	def outOfBound(self, x: int, y: int) -> bool:
		if x < 0 or x > self.rowDimension or y < 0 or y > self.colDimension:
			return True
		return False



#	while !(self.frontier.empty()):
#            tile = pop(self.frontier)
#            tilex = tile//10;
#            tiley = tile%10;
#            return Action(AI.Action.UNCOVER, startX, st)

