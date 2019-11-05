import numpy as np

def dynprof(alphabet, subMat, a, b):
    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]
    dirMat = lst[1]

    result = getBestMatching(scoMat, dirMat, a, b)

    for i in range(0, len(scoMat)):
        print(scoMat[i])

    for i in range(0, len(dirMat)):
        print(dirMat[i])

def populateScoringMatrix(alphabet, subMat, a, b):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)
    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            if(j - 1 == 0 and i - 1 == 0): diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[j - 1])][alphabet.index(b[i - 1])]
            elif (i - 1 == 0): diagonal = scoMat[i-1][j-1] + subMat[len(alphabet)][alphabet.index(b[i - 1])]
            elif (j - 1 == 0): diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[j - 1])][len(alphabet)]
            else: diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[j - 1])][alphabet.index(b[i - 1])]
            left = scoMat[i][j-1] + subMat[alphabet.index(a[j - 1])][len(alphabet)]
            up = scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(b[i - 1])]

            if(i == 1 and j == 1):
                print(alphabet.index(a[j - 1]))
                print(alphabet.index(b[i - 1]))
                print(subMat[alphabet.index(a[j - 1])][alphabet.index(b[i - 1])])
                print(diagonal)

            bestScore = max(diagonal, left, up)
            scoMat[i][j] = bestScore
            if bestScore == diagonal: dirMat[i][j] = "D"
            elif bestScore == up: dirMat[i][j] = "U"
            else: dirMat[i][j] = "L"
    return [scoMat, dirMat]

def initialiseScoringMatrix(alphabet, subMat, a, b):
    scoringMatrix = [[' ' for x in range(len(a) + 1)] for y in range(len(b) + 1)]
    scoringMatrix[0][0] = 0
    for x in range(1, len(b) + 1):
        scoringMatrix[x][0] = scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(b[x - 1])]
    for y in range(1, len(a) + 1):
        scoringMatrix[0][y] = scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(a[y - 1])]
    return scoringMatrix

def initialiseDirectionMatrix(alphabet, subMat, a, b):
    directionMatrix = [[' ' for x in range(len(a) + 1)] for y in range(len(b) + 1)]
    for x in range(1, len(b) + 1):
        directionMatrix[x][0] = "U"
    for y in range(1, len(a) + 1):
        directionMatrix[0][y] = "L"
    return directionMatrix

def getBestMatching(scoMat, dirMat, a, b):
    xPos = len(b)
    yPos = len(a)

    aMatch = []
    bMatch = []

    while(xPos != 0 and yPos != 0):
        if(dirMat[xPos][yPos] == "D"):
            aMatch = [yPos - 1] + aMatch
            bMatch = [xPos - 1] + bMatch
            yPos -= 1
            xPos -= 1
        elif(dirMat[xPos][yPos] == "U"):
            xPos -= 1
        else:
            yPos -= 1
    print(aMatch)
    print(bMatch)




a = [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]]
dynprof("ABC", a, "ABCACA", "BAACB")

print()

#Example from slides
#b = [[1,-1,-1,-1,-2],[-1,1,-1,-1,-2],[-1,-1,1,-1,-2],[-1,-1,-1,1,-2],[-2,-2,-2,-2,1]]
#dynprof("ACGT", b, "AGC", "AAAC") 

#c = [[2,-2,-2,-1,-1],[-2,2,-2,-2,-1],[-2,-2,2,-2,-1],[-2,-2,-2,2,-1],[-1,-1,-1,-1,2]]
#dynprof("ACGT", c, "CTCTGAG", "TGTCAGT") 