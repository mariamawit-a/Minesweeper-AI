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

from AI import AI
from Action import Action


class MyAI(AI):

    #class Tile(object):  # this is each tile on the local board
    #    __slots__ = ["state", "effectivelabel", "adjacentUnmarked"] # -2 for covered/unmarked, -1 for marked(mine), 0->infinity for uncovered label

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        self.X = startX
        self.Y = startY

        #class Tile(object):
        #    def __init__(self, state, effectivelabel, adjacentUnmarked):
        #        self.state = state
        #        self.effectivelabel = effectivelabel
        #        self.adjacentUnmarked = adjacentUnmarked

        self.board = [[-1 for i in range(rowDimension)]
                      for j in range(colDimension)]

        for col in self.board: #sets every tile to default, covered state as per model checking
            for row in col:
                row = "-2:0:0"

        self.move = 0
        self.uncovered = []
        self.uncoveredOnes = []
        self.frontier = []
        self.minefield = []

    def getAction(self, number: int) -> "Action Object":

        #print( "uncovered ", number, " on X: ", self.X," Y: ", self.Y)
        if self.move == 0:
            tile = self.startX * 10 + self.startY
            self.uncovered.append(tile)
            self.board[self.startX][self.startY] = 0
        else:
            self.board[self.Y][self.X] = number
            if number > 0:
                tile = self.X * 10 + self.Y
                self.uncoveredOnes.append(tile)

        if number == 0:
            self.addQueue(0, self.X, self.Y)
        else:
            self.addQueue(1, self.X, self.Y)

        if self.frontier:
            tile = self.frontier.pop()
            self.X = tile//10
            self.Y = tile % 10
            self.uncovered.append(tile)
            self.move += 1
            return Action(AI.Action.UNCOVER, self.X, self.Y)
        else:
            if len(self.minefield) > self.totalMines:
                tile = self.minMinefield()
                #tile = self.minefield.pop()
                self.X = tile//10
                self.Y = tile % 10
                self.uncovered.append(tile)
                self.move += 1
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

    def inBound(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.colDimension or y < 0 or y >= self.rowDimension:
            return False
        return True

    # b = 0 => frontier and b = 1 => minefield
    def addQueue(self, b: int, X: int, Y: int):
        # add top left
        if self.inBound(self.X-1, self.Y+1):
            tile = (self.X - 1) * 10 + (self.Y + 1)
            if tile not in self.uncovered:
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
        if self.inBound(self.X-1, self.Y+1):
            tile = (self.X - 1) * 10 + (self.Y)
            if tile not in self.uncovered:
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
        if self.inBound(self.X-1, self.Y-1):
            tile = (self.X - 1) * 10 + (self.Y-1)
            if tile not in self.uncovered:
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
        if self.inBound(self.X, self.Y+1):
            tile = (self.X) * 10 + (self.Y + 1)
            if tile not in self.uncovered:
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
        if self.inBound(self.X, self.Y-1):
            tile = (self.X) * 10 + (self.Y - 1)
            if tile not in self.uncovered:
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
        if self.inBound(self.X+1, self.Y+1):
            tile = (self.X + 1) * 10 + (self.Y + 1)
            if tile not in self.uncovered:
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
        if self.inBound(self.X+1, self.Y):
            tile = (self.X + 1) * 10 + (self.Y)
            if tile not in self.uncovered:
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
        if self.inBound(self.X+1, self.Y-1):
            tile = (self.X + 1) * 10 + (self.Y - 1)
            if tile not in self.uncovered:
                if b == 0:
                    if tile in self.minefield:
                        self.minefield.remove(tile)
                    if tile not in self.frontier:
                        self.frontier.append(tile)
                if b == 1:
                    if tile not in self.frontier:
                        if tile not in self.minefield:
                            self.minefield.append(tile)

    #removes the item with the smallest number of adjacent uncovered, numbered tiles from minefield (this is also
    #removed on the board in the function that calles it (this part must change->should be done here))
    def minMinefield(self) -> int:
        minOnes = 9
        for item in self.minefield:
            if self.numOnes(item) < minOnes:
                minOnes = self.numOnes(item)
                minItem = item
        self.minefield.remove(minItem)
        return minItem

    #finds the number of adjacent numbered tiles to a covered tile
    def numOnes(self, item: int) -> int:
        counter = 0
        tileX = item//10
        tileY = item % 10

        for ones in self.uncoveredOnes:
            onesTileX = ones // 10
            onesTileY = ones % 10
            thisX = tileX - onesTileX
            thisY = tileY - onesTileY

            if -1 <= thisX <= 1 and -1 <= thisY <= 1:
                counter += 1
        return counter



