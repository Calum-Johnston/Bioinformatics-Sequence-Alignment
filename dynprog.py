import numpy as np

def dynprof(alphabet, subMat, a, b):
    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]
    dirMat = lst[1]
    for i in range(0, len(scoMat)):
        print(scoMat[i])

    for i in range(0, len(dirMat)):
        print(dirMat[i])

def populateScoringMatrix(alphabet, subMat, a, b):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)
    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            bestScore = max(scoMat[i-1][j-1] + subMat[alphabet.index(a[j - 1])][alphabet.index(b[i - 1])], 
                            scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(a[j - 1])],
                            scoMat[i][j-1] + subMat[len(alphabet)][alphabet.index(b[i - 1])])
            scoMat[i][j] = bestScore
            if bestScore == scoMat[i-1][j-1] + subMat[alphabet.index(a[j - 1])][alphabet.index(b[i - 1])]: dirMat[i][j] = "D"
            elif bestScore == scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(a[j - 1])]: dirMat[i][j] = "U"
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





a = [[1,-1,-2,-1],[-1,2,-4.-1],[-2,-4,3,-2],[-1,-1,-2,0]]
dynprof("ABC", a, "ABCACA", "BAACB")

print()

b = [[]]
dynprof
