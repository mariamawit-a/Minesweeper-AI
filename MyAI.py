# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Mariamawit and Jacob
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
#import numpy as np
import signal



class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        self.X = startX
        self.Y = startY

        self.board = []
        for r in range(rowDimension):
            row = []
            for c in range(colDimension):
                state = -2
                effectiveLabel = 0
                adjacentUnmarked = 0

                if self.inBound([c-1, r-1]):
                    adjacentUnmarked += 1
                if self.inBound([c-1, r]):
                    adjacentUnmarked += 1
                if self.inBound([c-1, r+1]):
                    adjacentUnmarked += 1
                if self.inBound([c, r-1]):
                    adjacentUnmarked += 1
                if self.inBound([c, r+1]):
                    adjacentUnmarked += 1
                if self.inBound([c+1, r-1]):
                    adjacentUnmarked += 1
                if self.inBound([c+1, r]):
                    adjacentUnmarked += 1
                if self.inBound([c+1, r+1]):
                    adjacentUnmarked += 1

                tile = str(state)+":"+str(effectiveLabel) + ":"+str(adjacentUnmarked)
                row.append(tile)

            self.board.append(row)

        self.move = 0
        self.uncoveredFrontier = []
        self.uncoveredFrontierEffective = []
        self.coveredFrontier = []
        self.mines = []
        self.noMines = []
        self.uncoverAllFlag = False
        self.LocaluncoveredFrontier = []
        self.LocalcoveredFrontier = []
        self.recursion = 0
    def getAction(self, number: int) -> "Action Object":

        self.setState([self.X, self.Y], number, 0)
        self.setEffective([self.X, self.Y], self.getEffective([self.X, self.Y], 0) + number, 0)
        self.actionOnNeighbors(2, [self.X, self.Y])
        print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.board]))

        print("79 uncovered ", number, " on X: ", self.X, " Y: ", self.Y)
        # input("Press Enter to continue...")
        print("\n")

        if self.uncoverAllFlag:
            if self.noMines:
                #print("85 uncovering all within noMines ",self.noMines,"\n")
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                #print("90 trying to uncover X: ", self.X, " Y: ", self.Y)
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        elif number == 0:
            self.actionOnNeighbors(0, [self.X, self.Y])

        else:  # number != 0
            # E = 0
            if self.getEffective([self.X, self.Y], 0) == 0:
                self.actionOnNeighbors(0, [self.X, self.Y])

            # E = A
            elif self.getEffective([self.X, self.Y], 0) == self.getAdjacent([self.X, self.Y], 0):
                #print("105 calling NeighborsMines")
                self.NeighborsMines([self.X, self.Y])

            # E<A
            else:
                if [self.X, self.Y] not in self.uncoveredFrontier:
                    self.uncoveredFrontier.append([self.X, self.Y])
                #print("uncovered frontier",self.uncoveredFrontier, "\n")
                #print("covered frontier", self.coveredFrontier, "\n")
                #print("noMines 114 ", self.noMines, '\n')
                self.actionOnNeighbors(1, [self.X, self.Y])

           # #print('\n'.join([''.join(['{:8}'.format(item)
             #                           for item in row]) for row in self.board]))

        if self.uncoverAllFlag:
            if self.noMines:
                #print("122 uncovering all within noMines ",self.noMines,"\n")
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                #print("127 trying to uncover X: ", self.X, " Y: ", self.Y)
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        if self.noMines:
            tile = self.noMines.pop(0)
            self.X = tile[0]
            self.Y = tile[1]
            self.move += 1
            #print("137 trying to uncover X: ", self.X, " Y: ", self.Y)
            return Action(AI.Action.UNCOVER, self.X, self.Y)

        else:
            #print("uncovered frontier", self.uncoveredFrontier, "\n")
            #print("covered frontier", self.coveredFrontier, "\n")

            if len(self.coveredFrontier) <= 15:
                self.LocaluncoveredFrontier = self.uncoveredFrontier.copy()
                self.LocalcoveredFrontier = self.coveredFrontier.copy()

            else:
                self.LocaluncoveredFrontier = []
                self.LocalcoveredFrontier = [self.coveredFrontier[0].copy()]

                currentLengthCovered = 0
                currentLengthUncovered = 0

                while len(self.LocalcoveredFrontier) > currentLengthCovered:

                    if currentLengthCovered == 0:
                        currentLengthCovered += 0

                    self.actionOnNeighbors(
                        7, self.LocalcoveredFrontier[currentLengthCovered-1])

                    while len(self.LocaluncoveredFrontier) > currentLengthUncovered:
                        self.actionOnNeighbors(
                            8, self.LocaluncoveredFrontier[currentLengthUncovered-1])

                        currentLengthUncovered += 1

                    currentLengthCovered += 1

            covered_difference = [item for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]
            if 0 < len(covered_difference) < len(self.LocalcoveredFrontier):
                self.LocalcoveredFrontier = covered_difference
                uncovered_difference = [item for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
                self.LocaluncoveredFrontier = uncovered_difference


            #print("Localuncovered frontier", self.LocaluncoveredFrontier, "\n")
            #print("Localcovered frontier", self.LocalcoveredFrontier, "\n")

            #print("Enter model checking")

            return self.modelCheck()

    def actionOnNeighbors(self, b: int, cord: list):

        neighbors = [
            [cord[0]-1, cord[1]+1],
            [cord[0]-1, cord[1]],
            [cord[0]-1, cord[1]-1],
            [cord[0], cord[1]+1],
            [cord[0], cord[1]-1],
            [cord[0]+1, cord[1]+1],
            [cord[0]+1, cord[1]],
            [cord[0]+1, cord[1]-1],
        ]

        for neighbor in neighbors:

            if self.inBound(neighbor):

                if b == 0:  # E = 0

                    if self.getState(neighbor, 0) == -2:  # if covered
                        ##print("covered neighbor ", neighbor, "\n")
                        self.addnoMines(neighbor)

                        # if uncovered and not mine
                    elif self.getState(neighbor, 0) > 0 and self.getAdjacent(neighbor, 0) > 0:
                        ##print("uncovered neighbor ", neighbor, "\n")
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)

                        if self.getAdjacent(neighbor, 0) == self.getEffective(neighbor, 0):
                            self.NeighborsMines(neighbor)

                if b == 1:  # E < A

                    if self.getState(neighbor, 0) == -2:  # if covered
                        if neighbor not in self.noMines and neighbor not in self.mines and neighbor not in self.coveredFrontier:
                            self.coveredFrontier.append(neighbor)
                            #print("215 added ",neighbor," to coveredFrontier \n")

                    # if not mine and has uncovered neighbor
                    elif self.getState(neighbor, 0) > 0 and self.getAdjacent(neighbor, 0) != 0:
                        # #print("uncovered neighbor ", neighbor, "\n")
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)
                            #print("222 Neighbors of ", neighbor, " added to noMines \n")

                        if self.getAdjacent(neighbor, 0) == self.getEffective(neighbor, 0):
                            self.NeighborsMines(neighbor)
                            #print("226 Neighbors of ", neighbor, " added to Mines \n")

                if b == 2:  # called after action of uncovering a tile

                    self.setAdjacent(neighbor, self.getAdjacent(neighbor, 0) - 1, 0)

                if b == 3:  # called by NeighborsSafe

                    if self.getState(neighbor, 0) == -2:  # if covered
                        self.addnoMines(neighbor)

                if b == 4:  # called by NeighborsMines

                    if self.getState(neighbor, 0) == -2:  # if covered
                        #print("240 passing ", neighbor, " to addMine")
                        self.addMine(neighbor)

                if b == 5:  # called for Neighbor's of Mines

                    self.setAdjacent(neighbor, self.getAdjacent(neighbor, 0) - 1, 0)

                    # if not a mine
                    if neighbor not in self.mines:
                        self.setEffective(neighbor, self.getEffective(neighbor, 0) - 1, 0)

                    if neighbor in self.uncoveredFrontier:
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)


                if b == 6:  # called after adding bombs from permutation

                    if neighbor in self.LocaluncoveredFrontier:
                        index = self.LocaluncoveredFrontier.index(neighbor)
                        self.uncoveredFrontierEffective[index] -= 1

                    ##print("returns true")
                    #return True
                if b == 7:  # called to add neighbor of a LocalcoveredFrontier into LocaluncoveredFrontier

                    if neighbor in self.uncoveredFrontier and neighbor not in self.LocaluncoveredFrontier:
                        self.LocaluncoveredFrontier.append(neighbor.copy())

                if b == 8:  # called to add neighbor of a LocaluncoveredFrontier into LocalcoveredFrontier

                    if neighbor in self.coveredFrontier and neighbor not in self.LocalcoveredFrontier:
                        self.LocalcoveredFrontier.append(neighbor.copy())

    def NeighborsSafe(self, cord: list):
        if cord in self.uncoveredFrontier:
            self.uncoveredFrontier.remove(cord)
        self.actionOnNeighbors(3, cord)

    def NeighborsMines(self, cord: list):
        if cord in self.uncoveredFrontier:
            self.uncoveredFrontier.remove(cord)
        self.actionOnNeighbors(4, cord)

    def addnoMines(self, cord: list):
        if cord not in self.noMines:
            self.noMines.append(cord)
        if cord in self.coveredFrontier:
            self.coveredFrontier.remove(cord)
        #print("290 noMines", self.noMines, "\n")

    def addMine(self, cord: list):
        if cord in self.noMines:
            self.noMines.remove(cord)
        if cord in self.coveredFrontier:
            self.coveredFrontier.remove(cord)
        if cord not in self.mines:
            #print("296 adding ", cord, " to addMine")
            self.mines.append(cord)
            self.setState(cord, -1, 0)
            self.actionOnNeighbors(5, cord)
            #print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.board]))

            #print("\n")

            if self.totalMines == len(self.mines):
                #print("306 uncoverall called \n")
                self.uncoverAll()

    def setState(self, cord: list, state: int, type: int):
        cord1 = self.rowDimension - cord[1] - 1
        if type == 0:
            tile = self.board[cord1][cord[0]]
            tile = tile.split(":")
            tile[0] = str(state)
            self.board[cord1][cord[0]] = ':'.join(tile)
        else:
            tile = self.copyBoard[cord1][cord[0]]
            tile = tile.split(":")
            tile[0] = str(state)
            self.copyBoard[cord1][cord[0]] = ':'.join(tile)

    def getState(self, cord: list, type: int) -> int:
        cord1 = self.rowDimension - cord[1] - 1
        if type == 0:
            tile = self.board[cord1][cord[0]]
        else:
            tile = self.copyBoard[cord1][cord[0]]
        tile = tile.split(":")
        return int(tile[0])

    def setEffective(self, cord: list, E: int, type: int):
        cord1 = self.rowDimension - cord[1] - 1
        if type == 0:
            tile = self.board[cord1][cord[0]]
            tile = tile.split(":")
            tile[1] = str(E)
            self.board[cord1][cord[0]] = ':'.join(tile)
        else:
            tile = self.copyBoard[cord1][cord[0]]
            tile = tile.split(":")
            tile[1] = str(E)
            self.copyBoard[cord1][cord[0]] = ':'.join(tile)

    def getEffective(self, cord: list, type: int) -> int:
        cord1 = self.rowDimension - cord[1] - 1

        if type == 0:
            tile = self.board[cord1][cord[0]]
        else:
            tile = self.copyBoard[cord1][cord[0]]
        tile = tile.split(":")
        return int(tile[1])

    def setAdjacent(self, cord: list, A: int, type: int):
        cord1 = self.rowDimension - cord[1] - 1
        ##print("Decreasing adjacent uncover of row: ",cord1, " col: ", cord[0]," \n")

        if type == 0:
            tile = self.board[cord1][cord[0]]
            tile = tile.split(":")
            tile[2] = str(A)
            self.board[cord1][cord[0]] = ':'.join(tile)
        else:
            tile = self.copyBoard[cord1][cord[0]]
            tile = tile.split(":")
            tile[2] = str(A)
            self.copyBoard[cord1][cord[0]] = ':'.join(tile)

    def getAdjacent(self, cord: list, type: int) -> int:
        cord1 = self.rowDimension - cord[1] - 1
        ##print("Get adjacent uncover of row: ", cord1, " col: ", cord[0], " \n")

        if type == 0:
            tile = self.board[cord1][cord[0]]
        else:
            tile = self.copyBoard[cord1][cord[0]]
        tile = tile.split(":")
        return int(tile[2])

    def inBound(self, cord: list) -> bool:
        if 0 <= cord[0] < self.colDimension and 0 <= cord[1] < self.rowDimension:
            return True
        return False

    def uncoverAll(self):
        #add all uncovered tiles to no mine
        for X in range(self.colDimension):
            for Y in range(self.rowDimension):
                if self.getState([X, Y], 0) == -2 and [X, Y] not in self.noMines:  # if covered
                    self.noMines.append([X, Y])

        self.uncoverAllFlag = True
        # #print("added all uncovered to no mines ", self.noMines, "\n")
        # if self.noMines:
        #     tile = self.noMines.pop(0)
        #     self.X = tile[0]
        #     self.Y = tile[1]
        #     self.move += 1
        #     #print("trying to uncover X: ", self.X, " Y: ", self.Y)
        #     return Action(AI.Action.UNCOVER, self.X, self.Y)
        # else:
        #     return Action(AI.Action.LEAVE)

    def modelCheck(self):
        #print("405 in model check \n")
        self.recursion += 1
        #permutations = self.generate()
        #self.copyBoard = np.copy(self.board)

        self.uncoveredFrontierEffective = []
        for tile in self.LocaluncoveredFrontier:
            self.uncoveredFrontierEffective.append(self.getEffective(tile, 0))

        possible = []
        #print("415 about to iterate permutations \n")

        n = len(self.LocalcoveredFrontier)
        A = [-1, 0]
        index_of = {x: i for i, x in enumerate(A)}
        s = [A[0]] * n
        while True:
            p = list(s)
            ##print("trying permutation ", p)
            for i in range(len(self.LocalcoveredFrontier)):
                if p[i] == -1:
                    c = self.LocalcoveredFrontier[i]
                    #self.setState(c, -1, 1)
                    self.actionOnNeighbors(6, c)
                    ##print("set bomb on ", self.LocalcoveredFrontier[i])

            # #print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.copyBoard]))
            # #print("\n")
           # #print("effective is ", self.uncoveredFrontierEffective)
            if self.isValidPermutation():
                possible.append(p)
                print(p, " is a possible permutation")

            #self.copyBoard = np.copy(self.board)
            self.uncoveredFrontierEffective = []
            ##print("440 local uncovered frontier", self.LocaluncoveredFrontier)
            for tile in self.LocaluncoveredFrontier:
                self.uncoveredFrontierEffective.append(self.getEffective(tile, 0))

            for i in range(1, n + 1):
                if s[-i] == A[-1]:  # Last letter of alphabet, can not increment
                    s[-i] = A[0]
                else:
                    s[-i] = A[index_of[s[-i]] + 1]  # Modify to next letter
                    break
            else:
                break

        # for p in permutations:
        #     # #print("trying permutation ", p)
        #     for i in range(len(self.coveredFrontier)):
        #         if p[i] == -1:
        #             c = self.coveredFrontier[i]
        #             #self.setState(c, -1, 1)
        #             if self.actionOnNeighbors(6, c) == False:
        #                 break

        #     #         #print("set bomb on ", self.coveredFrontier[i])

        #     # #print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.copyBoard]))
        #     # #print("\n")
        #     if self.isValidPermutation():
        #         possible.append(p)
        #         ##print(p," is a possible permutation")
        #         #input("Press Enter to continue...")
        #     #self.copyBoard = np.copy(self.board)
        #     self.uncoveredFrontierEffective = []
        #     for tile in self.uncoveredFrontier:
        #         self.uncoveredFrontierEffective.append(self.getEffective(tile, 0))
        #print("number of possible permutation", len(possible))
        if(len(possible) == 0):
            #covered_difference = [item for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]
            self.LocalcoveredFrontier = self.coveredFrontier
            #uncovered_difference = [item for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
            self.LocaluncoveredFrontier = self.uncoveredFrontier
            return self.modelCheck()

        if len(possible) == 1:
            #print("477 possible is just 1 ", possible[0])
            p = possible[0]
            for i in range(len(self.LocalcoveredFrontier)):
                    if p[i] == 0:
                        #print("481 no mine on", self.LocalcoveredFrontier[i])
                        #print("481 LocalcoveredFrontier", self.LocalcoveredFrontier)
                        self.addnoMines(self.LocalcoveredFrontier[i])
                        #print("481 LocalcoveredFrontier", self.LocalcoveredFrontier)
                        #break;
                    if self.LocalcoveredFrontier == self.coveredFrontier:
                        if p[i] == -1:
                            #print("485 mine on", self.LocalcoveredFrontier[i])
                            #print("486 LocalcoveredFrontier", self.LocalcoveredFrontier)
                            self.addMine(self.LocalcoveredFrontier[i])
                            #print("488 LocalcoveredFrontier", self.LocalcoveredFrontier)


        else:
            sumindex = [sum(value) for value in zip(*possible)]
            max_value = max(sumindex)
            min_value = min(sumindex)

            if max_value == 0:
                for index in range(len(self.LocalcoveredFrontier)):
                    if sumindex[index] == 0 and self.LocalcoveredFrontier[index] not in self.mines:
                        acf = self.LocalcoveredFrontier[index]
                        print("494 adding ", self.LocalcoveredFrontier[index], "into no mine after model checking")
                        self.addnoMines(self.LocalcoveredFrontier[index])
                        #print("496 added ", self.LocalcoveredFrontier[index], "into no mine after model checking")
                        break
                #print("Finish adding noMines from MC")
            elif min_value == len(possible)*-1:
                for index in range(len(self.LocalcoveredFrontier)):
                    if sumindex[index] == min_value:
                        acf = self.LocalcoveredFrontier[index]
                        print("494 adding ", self.LocalcoveredFrontier[index], "into mine after model checking")
                        self.addMine(self.LocalcoveredFrontier[index])
                        #print("496 added ", self.LocalcoveredFrontier[index], "into mine after model checking")
                        break
                #print("Finish adding noMines from MC")
            else:
                print("taking a guess")
                max_index = sumindex.index(max_value)
                self.addnoMines(self.LocalcoveredFrontier[max_index])


        if self.noMines:
            #print("no mines 545, ", self.noMines, "\n")
            tile = self.noMines.pop(0)
            self.X = tile[0]
            self.Y = tile[1]
            #print("trying to uncover X: 545", self.X, " Y: ", self.Y)
            self.recursion = 0
            return Action(AI.Action.UNCOVER, self.X, self.Y)

        elif len(self.mines) == self.totalMines:
            #add all uncovered tiles to no mine
            for X in range(self.colDimension):
                for Y in range(self.rowDimension):
                    if self.getState([X, Y], 0) == -2 and [X, Y] not in self.noMines:  # if covered
                        self.noMines.append([X, Y])

            self.uncoverAllFlag = True
            print("added all uncovered to no mines ", self.noMines, "\n")
            if self.noMines:
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                #print("trying to uncover X: ", self.X, " Y: ", self.Y)
                self.recursion = 0
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        else:
            if self.recursion > 3:
                self.recursion = 0
                print("guess")
                return Action(AI.Action.UNCOVER, self.coveredFrontier[len(self.coveredFrontier)-len(self.coveredFrontier)//2][0], self.coveredFrontier[len(self.coveredFrontier)-len(self.coveredFrontier)//2][1])
           # input("call mc from mcu")
            #covered_difference = [item for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]
            self.LocalcoveredFrontier = self.coveredFrontier
            #uncovered_difference = [item for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
            self.LocaluncoveredFrontier = self.uncoveredFrontier
            return self.modelCheck()

    def generate(self) -> list:
        n = len(self.LocalcoveredFrontier)
        A = [-1, 0]
        permutations = []
        index_of = {x: i for i, x in enumerate(A)}
        s = [A[0]] * n
        while True:
            permutations.append(list(s))
            for i in range(1, n + 1):
                if s[-i] == A[-1]:  # Last letter of alphabet, can not increment
                    s[-i] = A[0]
                else:
                    s[-i] = A[index_of[s[-i]] + 1]  # Modify to next letter
                    break
            else:
                break
        return permutations

    def isValidPermutation(self) -> bool:
        # for tile in self.uncoveredFrontier:
        #     if self.getEffective(tile, 1) != 0:
        #         return False
        # return True
        if all([v == 0 for v in self.uncoveredFrontierEffective]):
            return True
        return False

    def modelCheckUncover(self):
        self.recursion += 1

        if self.noMines:
            #print("no mines 545, ", self.noMines, "\n")
            tile = self.noMines.pop(0)
            self.X = tile[0]
            self.Y = tile[1]
            #print("trying to uncover X: 545", self.X, " Y: ", self.Y)
            self.recursion = 0
            return Action(AI.Action.UNCOVER, self.X, self.Y)

        elif len(self.mines) == self.totalMines:
            #add all uncovered tiles to no mine
            for X in range(self.colDimension):
                for Y in range(self.rowDimension):
                    if self.getState([X, Y], 0) == -2 and [X, Y] not in self.noMines:  # if covered
                        self.noMines.append([X, Y])

            self.uncoverAllFlag = True
            print("added all uncovered to no mines ", self.noMines, "\n")
            if self.noMines:
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                #print("trying to uncover X: ", self.X, " Y: ", self.Y)
                self.recursion = 0
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        else:
            if self.recursion > 2:
                self.recursion = 0
                print("guess")
                return Action(AI.Action.UNCOVER, self.coveredFrontier[len(self.coveredFrontier)-len(self.coveredFrontier)//2][0], self.coveredFrontier[len(self.coveredFrontier)-len(self.coveredFrontier)//2][1])
           # input("call mc from mcu")
            #covered_difference = [item for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]
            self.LocalcoveredFrontier = self.coveredFrontier
            #uncovered_difference = [item for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
            self.LocaluncoveredFrontier = self.uncoveredFrontier
            return self.modelCheck()
