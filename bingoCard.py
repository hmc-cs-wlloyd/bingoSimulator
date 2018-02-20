import random

class Cell:
    def __init__(self, value):
        self.number = value
        self.isFilled = False

    #this sets whether the cell is
    #filled in (i.e. its number has
    #been called.
    def setFilled(self, filled):
        self.isFilled = filled

    def isNumber(self, value):
        return ((not self.isFilled) and (self.number == value))


class Card:
    def __init__(self, free):
        self.hasFree = free
        self.generateCellArray()
        if self.hasFree:
            self.cellArray[2][2].setFilled(True)


    def generateCellArray(self):
        bNums = range(1, 16)
        iNums = range(16, 31)
        nNums = range(31, 46)
        gNums = range(46, 61)
        oNums = range(61, 76)
        numSources = [bNums, iNums, nNums, gNums, oNums]

        cellArray = []
        numRows = 5
        for i in range(numRows):
            row = []

            for j in range(len(numSources)):
                num = random.choice(numSources[j])
                numSources[j].remove(num) #numbers can't appear more than once on a bingo card
                newCell = Cell(num)
                row.append(newCell)

            cellArray.append(row)
        
        self.cellArray = cellArray

    #fills in the square holding the given number, if such a square exists
    def fillSquare(self, number):
        for i in range(len(self.cellArray)):
            for j in range(len(self.cellArray[i])):
                if self.cellArray[i][j].isNumber(number):
                    self.cellArray[i][j].setFilled(True)
                    break #number will only appear once, so this adds efficiency 

    def hasWon(self):
        bingoR = False
        bingoV = False
        bingoD = False
        usedFree = False
 
        #search for row bingos
        for i in range(len(self.cellArray)):
            rowBingo = True
            for j in range(len(self.cellArray[i])):
                if not self.cellArray[i][j].isFilled:
                    rowBingo = False
            if rowBingo:
                bingoR = True
                if i == 2:
                    usedFree = True
        
        #search for column bingos
        for j in range(len(self.cellArray)): #relies on square cards
            columnBingo = True
            for i in range(len(self.cellArray)):
                if not self.cellArray[i][j].isFilled:
                    columnBingo = False
            if columnBingo:
                bingoV = True
                if j == 2:
                    usedFree = True

        #search for diagonal bingos
        d1bingo = True
        d2bingo = True
        for i in range(len(self.cellArray)): #also relies on square cards
            if not self.cellArray[i][i].isFilled:
                d1bingo = False
            if not self.cellArray[i][len(self.cellArray[i]) - 1 - i].isFilled:
                d2bingo = False

        bingoD = (d1bingo or d2bingo)
        if bingoD:
            usedFree = True

        return bingoR, bingoV, bingoD, usedFree
        
    
    #utility function for printing cards as arrays so we can see what numbers
    #they have. Does not presently display whether the squares are filled in.
    def printCellArray(self):
        printableCellArray = []
        numRows = 5
        for i in range(numRows):
            printableRow = []

            for j in range(len(self.cellArray[i])):
                printableRow.append(self.cellArray[i][j].number)

            printableCellArray.append(printableRow)
        
        print printableCellArray
            
            
        
