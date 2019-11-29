# Hirschberg's Algorithm for local alignment
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm

# Base functions, acts as acontroller to other functions
def dynproglin(alphabet, subMat, a, b):
    maxV = NWScore_Max(a, b, alphabet, subMat)  
    minV = NWScore_Max(reverseList(a[:maxV[1][0]]), reverseList(b[:maxV[1][1]]), alphabet, subMat)
    aStart = len(a[:maxV[1][0]]) - minV[1][0]
    aEnd = maxV[1][0]
    bStart = len(b[:maxV[1][1]]) - minV[1][1]
    bEnd = maxV[1][1]
    localA = a[aStart:aEnd]
    localB = b[bStart:bEnd]
    RSTT = recurse(localA, localB, alphabet, subMat)
    return [maxV[0], RSTT[0], RSTT[1]]

########################################
## Advanced functions that perform more complex calculations
########################################

# Recursively builds up the best alignment of two sequences and returns them
def recurse(a, b, alphabet, subMat):
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

        aAlign_l, bAlign_1 = recurse(a[:aMid], b[:bMid], alphabet, subMat)
        aAlign_r, bAlign_r = recurse(a[aMid:], b[bMid:], alphabet, subMat)

        aAlign = aAlign_l + aAlign_r
        bAlign = bAlign_1 + bAlign_r


    return aAlign, bAlign

# Builds up the scoring matrix and returns the final row (based on size of a)
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

# Returns the position of the end of the best local alignment and the value of said alignment
def NWScore_Max(a, b, alphabet, subMat):
    # Initialise matrices and variables
    scoringMatrix = [[0 for x in range(len(b) + 1)] for y in range(2)]
    maxValue = 0
    maxValuePos = [0,0]

    # Initialises the first row to 0
    for y in range(1, len(b) + 1):
        scoringMatrix[0][y] = 0
    # Loops through each row (except 1st) and each column position 
    for x in range(1, len(a) + 1):
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
        
        # Updates maximum value and it's position
        tempMaxValue = max(scoringMatrix[1])
        if(maxValue < tempMaxValue):
            maxValue = tempMaxValue
            maxValuePos[0] = x
            maxValuePos[1] = scoringMatrix[1].index(maxValue)

        # Swaps row 1 and row 0 (in an effort to conserve memory)
        for z in range(0, len(b) + 1):
            scoringMatrix[0][z] = scoringMatrix[1][z]

    # Returns the maximum value and it's position
    return maxValue, maxValuePos


########################################
## Simple functions that perform simple tasks
########################################

# Reverses a list
def reverseList(lst):
    return lst[::-1]

# Prints a 2D list
def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])




########################################
## Function(s) performs a global alignment of two sequences a and b
########################################
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
                
                if bestScore == diagonal: 
                    dirMat[i][j] = "D"
                elif bestScore == up: 
                    dirMat[i][j] = "U"
                else: 
                    dirMat[i][j] = "L"

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
        xPos = len(a); yPos = len(b)
        aMatch = ""; bMatch = ""
        while(xPos > 0 or yPos > 0):
            if(dirMat[xPos][yPos] == "D"):
                aMatch = a[xPos - 1] + aMatch
                bMatch = b[yPos - 1] + bMatch
                xPos -= 1; yPos -= 1
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

b = dynproglin("ACT", [[1,-1,-1,-2],[-1,1,-1,-2],[-1,-1,1,-2],[-2,-2,-2,1]], "TAATA", "TACTAA")
print("Score:   ", b[0])
print("Indices: ", b[1],b[2])

#c = dynproglin("ACGT", [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]], "GACTTAC", "CGTGAATTCAT") 
#print("Score:   ", c[0])
#print("Indices: ", c[1],c[2])

#d = dynproglin("ACGT",  [[2,-1,-1,-1,-2],[-1,2,-1,-1,-2],[-1,-1,2,-1,-2],[-1,-1,-1,2,-2],[-2,-2,-2,-2,0]], "TGGGGGGT", "TAAAAAAT")
#print("Score:   ", d[0])
#print("Indices: ", d[1],d[2])

#e = dynproglin("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],
#"AACAAADAAAACAADAADAAA", "CDCDDD")
#print("Score:   ", e[0])
#print("Indices: ", e[1],e[2])

#f = dynproglin("ABCD",[[ 1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]],
#"DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
#print("Score:   ", f[0])
#print("Indices: ", f[1],f[2])