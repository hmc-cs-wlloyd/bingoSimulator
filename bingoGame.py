import random
import sys
import bingoCard
from collections import defaultdict

def generateCards(numCards, free):
    cardList = []
    for i in range(numCards):
        card = bingoCard.Card(free)
        cardList.append(card)
    return cardList

def runGame(numCards, useFree):

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
            winR, winV, winD = card.hasWon()
            if (winR or winV or winD):
                gameWon = True
    
    numWinners = 0
    winDict = defaultdict(int)
    #winDataList = []
    for card in cards:
        winData = card.hasWon()
        #winDataList.append(winData)
        if (winData[0] or winData[1] or winData[2]):
            numWinners += 1
            winDict[winData] += 1

    return numWinners, rounds, winDict, cards[0].hasWon()
    

if __name__ == "__main__":

    #collect command line arguments
    numGames = int(sys.argv[1])
    numCards = int(sys.argv[2])
    useFree = (sys.argv[3].lower() == "true")
    outFileName = sys.argv[4] #should be empty file

    #set up dictionary to record win patterns
    winDict = defaultdict(int)

    #open the file for the output data
    dataFile = open(outFileName, 'w')
    dataFile.write("GameNumber, numWinners, numRounds, cardOne, H, V, D, HV, VD, HD, HVD\n")
    
    for i in range(numGames):
        numWinners, rounds, winTypes, cardOne = runGame(numCards, useFree) 
        dataFile.write(str(i) + ", " + str(numWinners) + ", " + str(rounds) + ", " + str(cardOne) + 
                      ", " + str(winTypes[(True, False, False)]) + ", " + str(winTypes[(False, True, False)]) + 
                      ", " + str(winTypes[(False, False, True)]) + ", " + str(winTypes[(True, True, False)]) + 
                      ", " + str(winTypes[(False, True, True)]) + ", " + str(winTypes[(True, False, True)]) + 
                      ", " + str(winTypes[(True, True, True)]) + "\n")
        for winType in winTypes:
            winDict[winType] += winTypes[winType]
        #for data in winData:
        #    dataFile.write(", " + str(data))
        #dataFile.write("\n")

    dataFile.close()

    print "H wins: ", winDict[(True, False, False)]
    print "V wins: ", winDict[(False, True, False)]
    print "D wins: ", winDict[(False, False, True)]
    print "HV wins: ", winDict[(True, True, False)]
    print "VD wins: ", winDict[(False, True, True)]
    print "HD wins: ", winDict[(True, False, True)]
    print "HVD wins: ", winDict[(True, True, True)]

    

    
