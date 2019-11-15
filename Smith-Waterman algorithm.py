# Smith-Waterman algorithm

def dynprog(alphabet, subMat, a, b):
    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
    alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
    scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
    return scoreAndAlignment

def populateScoringMatrix(alphabet, subMat, a, b):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)
    maxValue = 0
    maxValuePosition = [0, 0]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[i - 1])][alphabet.index(b[j - 1])]
            up = scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(a[i - 1])]
            left = scoMat[i][j-1] + subMat[alphabet.index(b[j - 1])][len(alphabet)]
            bestScore = max(diagonal, left, up, 0)
            if bestScore == diagonal: dirMat[i][j] = "D"
            elif bestScore == up: dirMat[i][j] = "U"
            elif bestScore == left: dirMat[i][j] = "L"
            scoMat[i][j] = bestScore
            if(bestScore > maxValue):
                maxValue = bestScore; maxValuePosition[0] = i; maxValuePosition[1] = j
    return [scoMat, dirMat, maxValue, maxValuePosition]

def initialiseScoringMatrix(alphabet, subMat, a, b):
    scoringMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    scoringMatrix[0][0] = 0
    for x in range(1, len(a) + 1):
        scoringMatrix[x][0] = max(0, scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(a[x - 1])])   
    for y in range(1, len(b) + 1):
        scoringMatrix[0][y] = max(0, scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(b[y - 1])])
    return scoringMatrix

def initialiseDirectionMatrix(alphabet, subMat, a, b):
    directionMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    for x in range(1, len(a) + 1):
        directionMatrix[x][0] = "U"        
    for y in range(1, len(b) + 1):
        directionMatrix[0][y] = "L"
    return directionMatrix

def getBestMatching(scoMat, dirMat, a, b, maxValuePos):
    xPos = maxValuePos[0]; yPos = maxValuePos[1]
    print(xPos)
    print(yPos)
    aMatch = []; bMatch = []
    while(scoMat[xPos][yPos] != 0):
        if(dirMat[xPos][yPos] == "D"):
            aMatch = [xPos - 1] + aMatch
            bMatch = [yPos - 1] + bMatch
            xPos -= 1 ; yPos -= 1
        elif(dirMat[xPos][yPos] == "U"):
            xPos -= 1
        else:
            yPos -= 1
        
    return [aMatch, bMatch]    

def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])



# TEST CASES

#a = dynprog("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA")
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])

#b = dynprog("ACT", [[1,-1,-1,-2],[-1,1,-1,-2],[-1,-1,1,-2],[-2,-2,-2,1]], "TAATA", "TACTAA")
#print("Score:   ", b[0])
#print("Indices: ", b[1],b[2])

#c = dynprog("ACGT", [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]], "GACTTAC", "CGTGAATTCAT") 
#print("Score:   ", c[0])
#print("Indices: ", c[1],c[2])

#d = dynprog("ABC",  [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "ABCACA", "BAACB") 
#print("Score:   ", d[0])
#print("Indices: ", d[1],d[2])

#e = dynprog("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "AGTACGCA", "TATGC")
#print("Score:   ", e[0])
#print("Indices: ", e[1],e[2])

#f = dynprog("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "TGGGGGGT", "TAAAAAAT")
#print("Score:   ", f[0])
#print("Indices: ", f[1],f[2])
