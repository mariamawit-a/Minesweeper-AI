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
from random import randint


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

                tile = str(state)+":"+str(effectiveLabel) + \
                    ":"+str(adjacentUnmarked)
                row.append(tile)

            self.board.append(row)

        self.move = 1
        self.uncoveredFrontier = []
        self.uncoveredFrontierEffective = []
        self.uncoveredFrontierEffectiveCopy = []
        self.coveredFrontier = []
        self.mines = []
        self.noMines = []
        self.uncoverAllFlag = False
        self.LocaluncoveredFrontier = []
        self.LocalcoveredFrontier = []
        self.recursion = 0
        self.pruned = False

    def getAction(self, number: int) -> "Action Object":

        # if self.move == 1:
        #     if self.totalMines == 10:
        #         #print("Beginners")
        #     elif self.totalMines == 40:
        #         #print("Intermediate")
        #     else:
        #         #print("Expert")


        self.setState([self.X, self.Y], number, 0)
        self.setEffective([self.X, self.Y], self.getEffective(
            [self.X, self.Y], 0) + number, 0)
        self.actionOnNeighbors(2, [self.X, self.Y])
        ###print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.board]))

        ##print("79 uncovered ", number, " on X: ", self.X, " Y: ", self.Y)
        # input("Press Enter to continue...")

        # all left is no mines
        if self.uncoverAllFlag:
            if self.noMines:
                ###print("85 uncovering all within noMines ",self.noMines,"\n")
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                ###print("90 trying to uncover X: ", self.X, " Y: ", self.Y)
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        #all left is mine
        if self.move == self.rowDimension*self.colDimension-self.totalMines:
            return Action(AI.Action.LEAVE)

        elif number == 0:
            self.actionOnNeighbors(0, [self.X, self.Y])

        else:  # number != 0
            # E = 0
            if self.getEffective([self.X, self.Y], 0) == 0:
                self.actionOnNeighbors(0, [self.X, self.Y])

            # E = A
            elif self.getEffective([self.X, self.Y], 0) == self.getAdjacent([self.X, self.Y], 0):
                #####print("105 calling NeighborsMines")
                self.NeighborsMines([self.X, self.Y])

            # E<A
            else:
                if [self.X, self.Y] not in self.uncoveredFrontier:
                    self.uncoveredFrontier.append([self.X, self.Y])
                #####print("uncovered frontier",self.uncoveredFrontier, "\n")
                #####print("covered frontier", self.coveredFrontier, "\n")
                #####print("noMines 114 ", self.noMines, '\n')
                self.actionOnNeighbors(1, [self.X, self.Y])

           # #####print('\n'.join([''.join(['{:8}'.format(item)
             #                           for item in row]) for row in self.board]))

        if self.uncoverAllFlag:
            if self.noMines:
                ###print("122 uncovering all within noMines ",self.noMines,"\n")
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                #####print("127 trying to uncover X: ", self.X, " Y: ", self.Y)
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        if self.noMines:
            tile = self.noMines.pop(0)
            self.X = tile[0]
            self.Y = tile[1]
            self.move += 1
            #####print("137 trying to uncover X: ", self.X, " Y: ", self.Y)
            return Action(AI.Action.UNCOVER, self.X, self.Y)

        else:
            #####print("uncovered frontier", self.uncoveredFrontier, "\n")
            #####print("covered frontier", self.coveredFrontier, "\n")
            self.pruned = False

            if len(self.coveredFrontier) < 20:
                self.LocaluncoveredFrontier = self.uncoveredFrontier.copy()
                self.LocalcoveredFrontier = self.coveredFrontier.copy()

            else:
                self.LocaluncoveredFrontier = []
                self.LocalcoveredFrontier = [self.coveredFrontier[0].copy()]

                currentLengthCovered = 0
                currentLengthUncovered = 0

                ##print("here")
                while len(self.LocalcoveredFrontier) > currentLengthCovered:

                    self.actionOnNeighbors(7, self.LocalcoveredFrontier[currentLengthCovered])

                    while len(self.LocaluncoveredFrontier) > currentLengthUncovered:
                        self.actionOnNeighbors(8, self.LocaluncoveredFrontier[currentLengthUncovered])

                        currentLengthUncovered += 1

                    currentLengthCovered += 1


            covered_difference = [item.copy() for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]

            if 0 < len(covered_difference) < len(self.LocalcoveredFrontier):
                self.LocalcoveredFrontier = covered_difference
                uncovered_difference = [item.copy() for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
                self.LocaluncoveredFrontier = uncovered_difference

            if len(self.LocalcoveredFrontier) > 19:
                while len(self.LocalcoveredFrontier) > 19:
                    self.LocalcoveredFrontier = []
                    self.LocaluncoveredFrontier = self.LocaluncoveredFrontier[:-1]
                    currentLengthUncovered = 0
                    while len(self.LocaluncoveredFrontier) > currentLengthUncovered:
                            self.actionOnNeighbors(8, self.LocaluncoveredFrontier[currentLengthUncovered])
                            currentLengthUncovered += 1
                self.pruned = True
                # #print("pruned Localuncovered frontier", self.LocaluncoveredFrontier, "\n")
                # #print("pruned Localcovered frontier", self.LocalcoveredFrontier, "\n")

                #####print("Enter model checking")

            return self.modelCheck()

    def neighborsinUncoveredFrontier(self, cord: list) -> bool:
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
            if neighbor in self.uncoveredFrontier and neighbor not in self.LocaluncoveredFrontier:
                 return False
        return True

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

                if b == 7:  # called to add neighbor of a LocalcoveredFrontier into LocaluncoveredFrontier

                    if neighbor in self.uncoveredFrontier and neighbor not in self.LocaluncoveredFrontier:
                        self.LocaluncoveredFrontier.append(neighbor.copy())

                elif b == 8:  # called to add neighbor of a LocaluncoveredFrontier into LocalcoveredFrontier

                    if neighbor in self.coveredFrontier and neighbor not in self.LocalcoveredFrontier:
                        self.LocalcoveredFrontier.append(neighbor.copy())

                elif b == 0:  # E = 0

                    if self.getState(neighbor, 0) == -2:  # if covered
                        ######print("covered neighbor ", neighbor, "\n")
                        self.addnoMines(neighbor)

                        # if uncovered and not mine
                    elif self.getState(neighbor, 0) > 0 and self.getAdjacent(neighbor, 0) > 0:
                        ######print("uncovered neighbor ", neighbor, "\n")
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)

                        if self.getAdjacent(neighbor, 0) == self.getEffective(neighbor, 0):
                            self.NeighborsMines(neighbor)

                elif b == 1:  # E < A

                    if self.getState(neighbor, 0) == -2:  # if covered
                        if neighbor not in self.noMines and neighbor not in self.mines and neighbor not in self.coveredFrontier:
                            self.coveredFrontier.append(neighbor)
                            #####print("215 added ",neighbor," to coveredFrontier \n")

                    # if not mine and has uncovered neighbor
                    elif self.getState(neighbor, 0) > 0 and self.getAdjacent(neighbor, 0) != 0:
                        # #####print("uncovered neighbor ", neighbor, "\n")
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)
                            #####print("222 Neighbors of ", neighbor, " added to noMines \n")

                        if self.getAdjacent(neighbor, 0) == self.getEffective(neighbor, 0):
                            self.NeighborsMines(neighbor)
                            #####print("226 Neighbors of ", neighbor, " added to Mines \n")

                elif b == 2:  # called after action of uncovering a tile

                    self.setAdjacent(neighbor, self.getAdjacent(neighbor, 0) - 1, 0)

                elif b == 3:  # called by NeighborsSafe

                    if self.getState(neighbor, 0) == -2:  # if covered
                        self.addnoMines(neighbor)

                elif b == 4:  # called by NeighborsMines

                    if self.getState(neighbor, 0) == -2:  # if covered
                        #####print("240 passing ", neighbor, " to addMine")
                        self.addMine(neighbor)

                elif b == 5:  # called for Neighbor's of Mines

                    self.setAdjacent(
                        neighbor, self.getAdjacent(neighbor, 0) - 1, 0)

                    # if not a mine
                    if neighbor not in self.mines:
                        self.setEffective(
                            neighbor, self.getEffective(neighbor, 0) - 1, 0)

                    if neighbor in self.uncoveredFrontier:
                        if self.getEffective(neighbor, 0) == 0:
                            self.NeighborsSafe(neighbor)

                elif b == 6:  # called after adding bombs from permutation

                    if neighbor in self.LocaluncoveredFrontier:
                        index = self.LocaluncoveredFrontier.index(neighbor)
                        self.uncoveredFrontierEffectiveCopy[index] -= 1

                    ######print("returns true")
                    #return True


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
        if cord in self.LocalcoveredFrontier:
            self.LocalcoveredFrontier.remove(cord)
        #####print("290 noMines", self.noMines, "\n")

    def addMine(self, cord: list):
        if cord in self.noMines:
            self.noMines.remove(cord)
        if cord in self.coveredFrontier:
            self.coveredFrontier.remove(cord)
        if cord in self.LocalcoveredFrontier:
            self.LocalcoveredFrontier.remove(cord)
        if cord not in self.mines:
            ##print("296 adding ", cord, " to addMine")
            self.mines.append(cord)
            self.setState(cord, -1, 0)
            self.actionOnNeighbors(5, cord)
            #####print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.board]))

            #####print("\n")

        if self.totalMines == len(self.mines):
            ###print("306 uncoverall called \n")
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
        ######print("Decreasing adjacent uncover of row: ",cord1, " col: ", cord[0]," \n")

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
        ######print("Get adjacent uncover of row: ", cord1, " col: ", cord[0], " \n")

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

    def modelCheck(self):
        ##print("405 in model check \n")
        self.recursion += 1

        self.uncoveredFrontierEffective = []
        self.uncoveredFrontierEffectiveCopy = []
        for tile in self.LocaluncoveredFrontier:
            effective = self.getEffective(tile, 0)
            self.uncoveredFrontierEffective.append(effective)
            self.uncoveredFrontierEffectiveCopy.append(effective)

        possible = []
        # ##print("415 about to iterate permutations \n")
        ###print("local uncovered ", self.LocaluncoveredFrontier)
        # ##print("uncovered ", self.uncoveredFrontier)
        ###print("local covered ", self.LocalcoveredFrontier)
        # ##print("covered ", self.coveredFrontier)
        # ##print("self.uncoveredFrontierEffective ", self.uncoveredFrontierEffective)
        n = len(self.LocalcoveredFrontier)
        #print("length of covered", n)

        if n == 0:
            return Action(AI.Action.LEAVE)
        # if n > 22:
        #     ##print("remove this")
        #     r = randint(0, len(self.coveredFrontier)-1)
        #     self.move += 1
        #     return Action(AI.Action.UNCOVER, self.coveredFrontier[r][0], self.coveredFrontier[r][1])

        A = [-1, 0]
        index_of = {x: i for i, x in enumerate(A)}
        s = [A[0]] * n
        while True:
            p = list(s)
            ###print("trying permutation ", p)
            for i in range(n):
                if p[i] == -1:
                    c = self.LocalcoveredFrontier[i]
                    #self.setState(c, -1, 1)
                    self.actionOnNeighbors(6, c)
                    ######print("set bomb on ", self.LocalcoveredFrontier[i])

            # #####print('\n'.join([''.join(['{:8}'.format(item) for item in row]) for row in self.copyBoard]))
            # #####print("\n")
            ###print("effective is ", self.uncoveredFrontierEffectiveCopy)
            if all([v == 0 for v in self.uncoveredFrontierEffectiveCopy]):
                possible.append(p)

            self.uncoveredFrontierEffectiveCopy = self.uncoveredFrontierEffective.copy()


            for i in range(1, n + 1):
                if s[-i] == A[-1]:  # Last letter of alphabet, can not increment
                    s[-i] = A[0]
                else:
                    s[-i] = A[index_of[s[-i]] + 1]  # Modify to next letter
                    break
            else:
                break

        #print(len(possible), " number of possible permutation")

        if(len(possible) == 0):
            ##print("nothing is possible")
            ##print("guess")
            #input("c")
            r = randint(0, len(self.LocalcoveredFrontier)-1)
            self.move += 1
            return Action(AI.Action.UNCOVER, self.LocalcoveredFrontier[r][0], self.LocalcoveredFrontier[r][1])

        mineadded = False
        if len(possible) == 1:
            ##print("477 possible is just 1 ", possible[0])
            p = possible[0]
            for i in reversed(range(len(self.LocalcoveredFrontier))):
                if p[i] == 0:
                    #####print("481 no mine on", self.LocalcoveredFrontier[i])
                    #####print("481 LocalcoveredFrontier", self.LocalcoveredFrontier)
                    acf = self.LocalcoveredFrontier[i]
                    if self.pruned == True and self.neighborsinUncoveredFrontier(acf) == False:
                        continue
                    self.addnoMines(acf)
                    #####print("481 LocalcoveredFrontier", self.LocalcoveredFrontier)
                    #break;
                # if len(self.LocalcoveredFrontier) >= len(self.coveredFrontier) - 5:
                #     if p[i] == -1:
                #         #####print("485 mine on", self.LocalcoveredFrontier[i])
                #         #####print("486 LocalcoveredFrontier", self.LocalcoveredFrontier)
                #         self.addMine(self.LocalcoveredFrontier[i])
                #         mineadded = True
                #         #####print("488 LocalcoveredFrontier", self.LocalcoveredFrontier)

        else:
            sumindex = [sum(value) for value in zip(*possible)]
            max_value = max(sumindex)
            min_value = min(sumindex)

            ##print("min value", min_value)
            ##print("max value", max_value)
            if max_value == 0:
                for index in reversed(range(len(self.LocalcoveredFrontier))):
                    if sumindex[index] == 0:
                        acf = self.LocalcoveredFrontier[index]
                        if self.pruned == True and self.neighborsinUncoveredFrontier(acf) == False:
                            continue
                        ##print("509 adding ", self.LocalcoveredFrontier[index], "into no mine after model checking")
                        self.addnoMines(acf)
                        ###print("496 added ", self.LocalcoveredFrontier[index], "into no mine after model checking")

                #####print("Finish adding noMines from MC")
            elif min_value == len(possible)*-1:
                for index in reversed(range(len(self.LocalcoveredFrontier))):
                    if sumindex[index] == min_value:
                        acf = self.LocalcoveredFrontier[index]
                        ##print("519 adding ", self.LocalcoveredFrontier[index], "into mine after model checking")
                        if self.pruned == True and self.neighborsinUncoveredFrontier(acf) == False:
                            continue
                        self.addMine(acf)
                        mineadded = True
                        ##print("522 added ", acf, "into mine after model checking")
                        #if self.pruned == True:
                        break
                #####print("Finish adding noMines from MC")
            elif len(possible) > 0 :
                #if len(self.LocalcoveredFrontier) == len(self.coveredFrontier):
                #print("577 taking a guess")
                possible_noMines = [i for i, n in enumerate(sumindex) if n == max_value and self.neighborsinUncoveredFrontier(
                    self.LocalcoveredFrontier[i])]

                if len(possible_noMines) > 0:
                    guess_index = possible_noMines[randint(0, len(possible_noMines)-1)]
                    self.addnoMines(self.LocalcoveredFrontier[guess_index])

        if self.noMines:
            #print("no mines 545, ", self.noMines, "\n")
            tile = self.noMines.pop(0)
            self.X = tile[0]
            self.Y = tile[1]
            ##print("trying to uncover X: 545", self.X, " Y: ", self.Y)
            self.move += 1
            self.recursion = 0
            return Action(AI.Action.UNCOVER, self.X, self.Y)

        elif len(self.mines) == self.totalMines:
            #add all uncovered tiles to no mine
            for X in range(self.colDimension):
                for Y in range(self.rowDimension):
                    if self.getState([X, Y], 0) == -2 and [X, Y] not in self.noMines:  # if covered
                        self.noMines.append([X, Y])

            self.uncoverAllFlag = True
            ##print("added all uncovered to no mines ", self.noMines, "\n")
            if self.noMines:
                tile = self.noMines.pop(0)
                self.X = tile[0]
                self.Y = tile[1]
                self.move += 1
                ##print("trying to uncover X: ", self.X, " Y: ", self.Y)
                self.recursion = 0
                return Action(AI.Action.UNCOVER, self.X, self.Y)
            else:
                return Action(AI.Action.LEAVE)

        else:
            if mineadded == True:
                #print("mine added")
                mineadded = False
                return self.modelCheck()
            elif self.recursion > 4 or len(self.LocalcoveredFrontier) == len(self.coveredFrontier):
                self.recursion = 0
                #print("571 guess")
                r = randint(0, len(self.LocalcoveredFrontier)-1)
                ####print("guess index", r)
                #input("cont")
                self.move += 1
                return Action(AI.Action.UNCOVER, self.LocalcoveredFrontier[r][0], self.LocalcoveredFrontier[r][1])
            else:
                #print("changed frontier")
                self.LocaluncoveredFrontier = []
                self.LocalcoveredFrontier = [[item.copy() for item in self.coveredFrontier if item not in self.LocalcoveredFrontier][0]]

                currentLengthCovered = 0
                currentLengthUncovered = 0

                ##print("here")
                while len(self.LocalcoveredFrontier) > currentLengthCovered:

                    self.actionOnNeighbors(
                        7, self.LocalcoveredFrontier[currentLengthCovered])

                    while len(self.LocaluncoveredFrontier) > currentLengthUncovered:
                        self.actionOnNeighbors(
                            8, self.LocaluncoveredFrontier[currentLengthUncovered])

                        currentLengthUncovered += 1

                    currentLengthCovered += 1

            covered_difference = [item.copy() for item in self.coveredFrontier if item not in self.LocalcoveredFrontier]

            if 0 < len(covered_difference) < len(self.LocalcoveredFrontier):
                self.LocalcoveredFrontier = covered_difference
                uncovered_difference = [item.copy() for item in self.uncoveredFrontier if item not in self.LocaluncoveredFrontier]
                self.LocaluncoveredFrontier = uncovered_difference

            if len(self.LocalcoveredFrontier) > 19:
                while len(self.LocalcoveredFrontier) > 19:
                    self.LocalcoveredFrontier = []
                    self.LocaluncoveredFrontier = self.LocaluncoveredFrontier[:-1]
                    currentLengthUncovered = 0
                    while len(self.LocaluncoveredFrontier) > currentLengthUncovered:
                        self.actionOnNeighbors(8, self.LocaluncoveredFrontier[currentLengthUncovered])
                        currentLengthUncovered += 1
                self.pruned = True
                #print("pruned Localuncovered frontier", self.LocaluncoveredFrontier, "\n")
                #print("pruned Localcovered frontier", self.LocalcoveredFrontier, "\n")

            return self.modelCheck()
    ################################################The functions bellow have been integrated to other functions hence not called#######################################################
    def generate(self) -> list:
        n = len(self.LocalcoveredFrontier)
        A = [-1, 0]
        permutations = []
        index_of = {x: i for i, x in enumerate(A)}
        s = [A[0]] * n
        while 1:
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
        if all([v == 0 for v in self.uncoveredFrontierEffective]):
            return True
        return False
