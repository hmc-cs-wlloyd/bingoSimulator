import random
import sys
import bingoCard
import itertools
from collections import defaultdict

def generateCards(numCards, free):
    cardList = []
    for i in range(numCards):
        card = bingoCard.Card(free)
        cardList.append(card)
    return cardList

def runGame(inTuple):
    numCards = inTuple[0]
    useFree = inTuple[1]

    #generate the cards for the game
    cards = generateCards(numCards, useFree)

    #generate pool from which numbers are drawn
    numberPool = range(1, 76)

    #run game until it is won
    gameWon = False
    rounds = 0
    while not gameWon:
        numberDrawn = random.choice(numberPool)
        numberPool.remove(numberDrawn)
        rounds += 1
        for card in cards:
            card.fillSquare(numberDrawn)
            winR, winV, winD, usedFree = card.hasWon()
            if (winR or winV or winD):
                gameWon = True
    
    numWinners = 0
    #winDict = defaultdict(int) #collect individual results for debug
    winType = (False, False, False)
    freeUsed = False
    for card in cards:
        winData = card.hasWon()
        winType = ((winType[0] or winData[0]), (winType[1] or winData[1]), (winType[2] or winData[2]))
        if (winData[0] or winData[1] or winData[2]):
            #winDict[winData] += 1 #collect individual results for debug
            numWinners += 1
            freeUsed |= useFree and winData[3]
            
        

    return numWinners, rounds, winType, freeUsed, cards[0].hasWon()#, winDict
    

if __name__ == "__main__":

    #collect command line arguments
    numGames = int(sys.argv[1])
    numCards = int(sys.argv[2])
    useFree = (sys.argv[3].lower() == "true")
    outFileName = sys.argv[4] #should be empty file

    #set up dictionary to record win patterns
    winDict = defaultdict(int)
    singleWinnerDict = defaultdict(int)
    usedFreeDict = defaultdict(int)
    dataTable = []

    #collect individual results for debug
    #winDataList = []
    
    pool = ThreadPool(1)
    dataTable = [runGame((numCards, useFree)) for i in range(numGames)]
    pool.close()
    pool.join()
        
    #note this tally separates wins of the same type that use/don't use free
    for data in dataTable:
        winDict[data[2]] += 1
        if data[0] == 1:
            singleWinnerDict[data[2]] += 1
        if data[3]:
            usedFreeDict[data[2]] += 1
        
        #collect individual results for debug 
        #winDataList.append(individualWins)
    
    #open the file for the output data
    dataFile = open(outFileName, 'w')
    dataFile.write("GameNumber, numWinners, numRounds, winType, usedFree, cardOne\n")

    counter = 0
    for row in dataTable:
        dataFile.write(str(counter))
        counter += 1
        for entry in row:
            dataFile.write(", ")
            dataFile.write(str(entry))
        dataFile.write("\n")
            

    dataFile.write("H wins: " + str(winDict[(True, False, False)]) + "\n")
    dataFile.write("H solo wins: " + str(singleWinnerDict[(True, False, False)]) + "\n")
    dataFile.write("H wins with free: " + str(usedFreeDict[(True, False, False)]) + "\n")
    dataFile.write("V wins: " + str(winDict[(False, True, False)]) + "\n")
    dataFile.write("V solo wins: " + str(singleWinnerDict[(False, True, False)]) + "\n")
    dataFile.write("V wins with free: " + str(usedFreeDict[(False, True, False)]) + "\n")
    dataFile.write("D wins: " + str(winDict[(False, False, True)]) + "\n")
    dataFile.write("D solo wins: " + str(singleWinnerDict[(False, False, True)]) + "\n")
    dataFile.write("D wins with free: " + str(usedFreeDict[(False, False, True)]) + "\n")
    dataFile.write("HV wins: " + str(winDict[(True, True, False)]) + "\n")
    dataFile.write("HV solo wins: " + str(singleWinnerDict[(True, True, False)]) + "\n")
    dataFile.write("HV wins with free: " + str(usedFreeDict[(True, True, False)]) + "\n")
    dataFile.write("VD wins: " + str(winDict[(False, True, True)]) + "\n")
    dataFile.write("VD solo wins: " + str(singleWinnerDict[(False, True, True)]) + "\n")
    dataFile.write("VD wins with free: " + str(usedFreeDict[(False, True, True)]) + "\n")
    dataFile.write("HD wins: " + str(winDict[(True, False, True)]) + "\n")
    dataFile.write("HD solo wins: " + str(singleWinnerDict[(True, False, True)]) + "\n")
    dataFile.write("HD wins with free: " + str(usedFreeDict[(True, False, True)]) + "\n")
    dataFile.write("HVD wins: " + str(winDict[(True, True, True)]) + "\n")
    dataFile.write("HVD solo wins: " + str(singleWinnerDict[(True, True, True)]) + "\n")
    dataFile.write("HVD wins with free: " + str(usedFreeDict[(True, True, True)]) + "\n")

    dataFile.close()
