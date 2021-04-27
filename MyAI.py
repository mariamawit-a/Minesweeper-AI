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

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	#pulls from either frontier or (if frontier is empty) minefield
	#uncovers that tile, and then adds adjacent covered tiles (that are not already in frontier or minefield) into them
	#	as appropriate
	#modifies the data for the tile in the 2d array
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
