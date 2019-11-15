# Hirschberg's Algorithm
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm

def Hirschberg(alphabet, subMat, a, b):

    def align(a, b, alphabet, subMat):
        aAlign, bAlign = "", ""

        if(len(a) == 0):
          for i in range(0, len(b)):
                aAlign + "-"
                bAlign += b[i]
        elif(len(b) == 0):
            for i in range(0, len(a)):
                aAlign += a[i]
                bAlign += "-"
        elif(len(a) == 1 or len(b) == 1):
            rst = NeedlanWunsch(alphabet, subMat, a, b)
            aAlign = rst[1]
            bAlign = rst[2]
        else:
            aMid = int(len(a) / 2)
            scoreL = NWScore(a[:aMid], b, alphabet, subMat)
            scoreR = NWScore(reverseList(a[aMid:]), reverseList(b), alphabet, subMat)
            temp = [x + y for x, y in zip(scoreL, reverseList(scoreR))]
            bMid = temp.index(max(temp))

            aAlign_l, bAlign_1 = align(a[:aMid], b[:bMid], alphabet, subMat)
            aAlign_r, bAlign_r = align(a[aMid:], b[bMid:], alphabet, subMat)

            aAlign = aAlign_l + aAlign_r
            bAlign = bAlign_1 + bAlign_r

        return aAlign, bAlign

    maxValueInfo = NWScore_maxValue(a, b, alphabet, subMat, True)
    print(maxValueInfo[1])
    print()
    minValueInfo = NWScore_maxValue(reverseList(a), reverseList(b), alphabet, subMat, False)
    print((len(a) - minValueInfo[1][0]) , " " , (len(b) - minValueInfo[1][1]))
    print()
    localA = a[(len(a) - minValueInfo[1][0]):maxValueInfo[1][0]]
    localB = b[(len(b) - minValueInfo[1][1]):maxValueInfo[1][1]]
    print(localA , "  ", localB)
    RSTT = align(localA, localB, alphabet, subMat)
    print(RSTT[0])
    print(RSTT[1])


def NWScore(a, b, alphabet, subMat):
    scoringMatrix = [[0 for x in range(len(b) + 1)] for y in range(2)]
    # Initialises first row
    for y in range(1, len(b) + 1):
        scoringMatrix[0][y] = scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(b[y - 1])]
    
    # Completes all rows but the first (0th)
    for x in range(1, len(a) + 1):
        # Completes all column positions (including 0th)
        for y in range(0, len(b) + 1):
            if(y == 0):
                scoringMatrix[1][y] = scoringMatrix[0][y] + subMat[len(alphabet)][alphabet.index(a[x - 1])]
            else:
                scoringMatrix[1][y] = max(
                    scoringMatrix[0][y-1] + subMat[alphabet.index(a[x - 1])][alphabet.index(b[y - 1])],
                    scoringMatrix[0][y] + subMat[len(alphabet)][alphabet.index(a[x - 1])],
                    scoringMatrix[1][y-1] + subMat[alphabet.index(b[y - 1])][len(alphabet)]
                )
        # Puts row 1 in row 0
        for z in range(0, len(b) + 1):
            scoringMatrix[0][z] = scoringMatrix[1][z]
    return scoringMatrix[1]


def NWScore_maxValue(a, b, alphabet, subMat, rev):
    scoringMatrix = [[0 for x in range(len(b) + 1)] for y in range(2)]
    maxValue = 0
    tempMaxValue = 0
    maxValuePos = [0,0]

    # Initialises first row
    for y in range(1, len(b) + 1):
        scoringMatrix[0][y] = 0
    print(scoringMatrix[0])
    
    # Completes all rows but the first (0th)
    for x in range(1, len(a) + 1):
        # Completes all column positions (including 0th)
        for y in range(0, len(b) + 1):
            if(y == 0):
                scoringMatrix[1][y] = 0
            else:
                scoringMatrix[1][y] = max(
                    scoringMatrix[0][y-1] + subMat[alphabet.index(a[x - 1])][alphabet.index(b[y - 1])],
                    scoringMatrix[0][y] + subMat[len(alphabet)][alphabet.index(a[x - 1])],
                    scoringMatrix[1][y-1] + subMat[alphabet.index(b[y - 1])][len(alphabet)],
                    0
                )

        if(rev == True):
            tempMaxValue = (max(scoringMatrix[1]))
            if(maxValue <= tempMaxValue):
                maxValue = tempMaxValue
                maxValuePos[0] = x
                maxValuePos[1] = len(scoringMatrix[1]) - 1 - reverseList(scoringMatrix[1]).index(tempMaxValue)
        else:
            if(tempMaxValue == 0):
                tempMaxValue = (max(scoringMatrix[1]))
                if(maxValue <= tempMaxValue):
                    maxValue = tempMaxValue
                    maxValuePos[0] = x
                    maxValuePos[1] = scoringMatrix[1].index(tempMaxValue)

        # Puts row 1 in row 0
        for z in range(0, len(b) + 1):
            scoringMatrix[0][z] = scoringMatrix[1][z]    
        print(scoringMatrix[1])  

    return maxValue, maxValuePos

def reverseList(lst):
    return lst[::-1]

def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])







def NeedlanWunsch(alphabet, subMat, a, b):

    def populateScoringMatrix(alphabet, subMat, a, b):
        scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
        dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                diagonal = scoMat[i-1][j-1] + subMat[alphabet.index(a[i - 1])][alphabet.index(b[j - 1])]
                up = scoMat[i-1][j] + subMat[len(alphabet)][alphabet.index(a[i - 1])]
                left = scoMat[i][j-1] + subMat[alphabet.index(b[j - 1])][len(alphabet)]
                bestScore = max(diagonal, left, up)
                if bestScore == diagonal: dirMat[i][j] = "D"
                elif bestScore == up: dirMat[i][j] = "U"
                else: dirMat[i][j] = "L"
                scoMat[i][j] = bestScore
        return [scoMat, dirMat]

    def initialiseScoringMatrix(alphabet, subMat, a, b):
        scoringMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
        scoringMatrix[0][0] = 0
        for x in range(1, len(a) + 1):
            scoringMatrix[x][0] = scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(a[x - 1])]   
        for y in range(1, len(b) + 1):
            scoringMatrix[0][y] = scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(b[y - 1])]
        return scoringMatrix

    def initialiseDirectionMatrix(alphabet, subMat, a, b):
        directionMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
        for x in range(1, len(a) + 1):
            directionMatrix[x][0] = "U"
        for y in range(1, len(b) + 1):
            directionMatrix[0][y] = "L"
        return directionMatrix

    def getBestMatching(scoMat, dirMat, a, b):
        xPos = len(a)
        yPos = len(b)
        aMatch = ""
        bMatch = ""
        while(xPos > 0 or yPos > 0):
            if(dirMat[xPos][yPos] == "D"):
                aMatch = a[xPos - 1] + aMatch
                bMatch = b[yPos - 1] + bMatch
                yPos -= 1
                xPos -= 1
            elif(dirMat[xPos][yPos] == "U"):
                aMatch = a[xPos - 1] + aMatch
                bMatch = "-" + bMatch
                xPos -= 1
            else:
                aMatch = "-" + aMatch
                bMatch = b[yPos - 1] + bMatch
                yPos -= 1
        return [aMatch, bMatch]
    
    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]
    dirMat = lst[1]
    alignment = getBestMatching(scoMat, dirMat, a, b)
    scoreAndAlignment = [scoMat[len(a)][len(b)], alignment[0], alignment[1]]
    return scoreAndAlignment


    

# TEST CASES

#a = dynproglin("ABC", [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "AABBAACA", "CBACCCBA")
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])

#b = dynproglin("ACT", [[1,-1,-1,-2],[-1,1,-1,-2],[-1,-1,1,-2],[-2,-2,-2,1]], "TAATA", "TACTAA")
#print("Score:   ", b[0])
#print("Indices: ", b[1],b[2])

#c = dynproglin("ACGT", [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]], "GACTTAC", "CGTGAATTCAT") 
#print("Score:   ", c[0])
#print("Indices: ", c[1],c[2])

#d = dynproglin("ABC",  [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]], "ABCACA", "BAACB") 
#print("Score:   ", d[0])
#print("Indices: ", d[1],d[2])

#e = Hirschberg("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "AGTACGCA", "TATGC")

e = Hirschberg("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "TGGGGGGT", "TAAAAAAT")
