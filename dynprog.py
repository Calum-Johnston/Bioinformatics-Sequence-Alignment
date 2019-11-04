import numpy as np

def dynprof(alphabet, subMat, a, b):
    scoMat = populateScoringMatrix(alphabet, subMat, a, b)

def populateScoringMatrix(alphabet, subMat, a, b):

    # Initialise the scoring matrix 
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)

   # for i in range(1, len(a)):
      #  for j in range(1, len(b)):
         #   bestScore = max(scoMat[i-1][j-1], scoMat[i-1][j], scoMat[i][j-1])

def initialiseScoringMatrix(alphabet, subMat, a, b):

    scoringMatrix = [[' ' for x in range(len(a) + 1)] for y in range(len(b) + 1)]
    for i in range(0, len(b)):
        print(scoringMatrix[i])
    scoringMatrix[0][0] = 0

    for x in range(1, len(b) + 1):
        subMat[len(alphabet)][alphabet.index(b[x - 1])]
        scoringMatrix[x][0] = scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(b[x - 1])]
    for y in range(1, len(a)):
        scoringMatrix[0][y] = scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(a[y - 1])]
    
    print(scoringMatrix)
    print()
    for i in range(0, len(b) + 1):
        print(scoringMatrix[i])

    return scoringMatrix




a = [[1,-1,-2,-1],[-1,2,-4.-1],[-2,-4,3,-2],[-1,-1,-2,0]]
dynprof("ABC", a, "ABCACA", "BAACB")
