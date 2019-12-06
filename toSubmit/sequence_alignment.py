import itertools
from operator import itemgetter
import numpy as np

# Smith-Waterman algorithm
def dynprog(alphabet, subMat, a, b):

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

    lst = populateScoringMatrix(alphabet, subMat, a, b)
    scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
    alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
    scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
    return scoreAndAlignment


# Hirschberg's Algorithm for local alignment
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm
# Base functions, acts as acontroller to other functions
def dynproglin(alphabet, subMat, a, b):

    ########################################
    ## Advanced functions that perform more complex calculations
    ########################################

    # Recursively builds up the best alignment of two sequences and returns them
    def recurse(a, b, alphabet, subMat, aStart, aEnd, bStart, bEnd):
        aAlign, bAlign = "", ""

        if(len(a) == 1 or len(b) == 1):
            rst = NeedlanWunsch(alphabet, subMat, a, b,  aEnd, bEnd)
            aAlign = rst[1]
            bAlign = rst[2]
        else:
            aMid = int(len(a) / 2)
            scoreL = NWScore(a[:aMid], b, alphabet, subMat)
            scoreR = NWScore(reverseList(a[aMid:]), reverseList(b), alphabet, subMat)
            temp = [x + y for x, y in zip(scoreL, reverseList(scoreR))]
            bMid = temp.index(max(temp))

            #print("1st = ", a[:aMid], b[:bMid], aStart, aStart + aMid, bStart, bStart + bMid)
        # print("2nd = ", a[aMid:], b[bMid:], aStart + aMid, aEnd, bStart + bMid, bEnd)

            aAlign_l, bAlign_1 = recurse(a[:aMid], b[:bMid], alphabet, subMat, aStart, aStart + aMid, bStart, bStart + bMid)
            aAlign_r, bAlign_r = recurse(a[aMid:], b[bMid:], alphabet, subMat, aStart + aMid, aEnd, bStart + bMid, bEnd)

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
    def NeedlanWunsch(alphabet, subMat, a, b, aEnd, bEnd):

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

        def getBestMatching(scoMat, dirMat, a, b, aEnd, bEnd):
            xPos = len(a); yPos = len(b)
            aMatch = []; bMatch = []
            while(xPos > 0 or yPos > 0):
                if(dirMat[xPos][yPos] == "D"):
                    aMatch = [aEnd - 1] + aMatch
                    bMatch = [bEnd - 1] + bMatch
                    xPos -= 1; yPos -= 1
                    aEnd -= 1; bEnd -= 1
                elif(dirMat[xPos][yPos] == "U"):
                    xPos -= 1; aEnd -= 1
                else:
                    yPos -= 1; bEnd -= 1
            return [aMatch, bMatch]
        
        lst = populateScoringMatrix(alphabet, subMat, a, b)
        scoMat = lst[0]
        dirMat = lst[1]
        alignment = getBestMatching(scoMat, dirMat, a, b, aEnd, bEnd)
        scoreAndAlignment = [scoMat[len(a)][len(b)], alignment[0], alignment[1]]
        return scoreAndAlignment

    maxV = NWScore_Max(a, b, alphabet, subMat)  
    minV = NWScore_Max(reverseList(a[:maxV[1][0]]), reverseList(b[:maxV[1][1]]), alphabet, subMat)
    aStart = len(a[:maxV[1][0]]) - minV[1][0]
    aEnd = maxV[1][0]
    bStart = len(b[:maxV[1][1]]) - minV[1][1]
    bEnd = maxV[1][1]
    localA = a[aStart:aEnd]
    localB = b[bStart:bEnd]
    RSTT = recurse(localA, localB, alphabet, subMat, aStart, aEnd, bStart, bEnd)
    return [maxV[0], RSTT[0], RSTT[1]]


# FASTA algorithm (Heuristic)
def heuralign(alphabet, subMat, a, b):
    
    # Initialises the index table
    def initialiseIndexTable(a, ktup):
        keywords = [''.join(i) for i in itertools.product("ABCD", repeat = ktup)]
        indexTable = {}
        for keyword in keywords:
            indexTable[keyword] = []
        for i in range(0, len(a) + 1 - ktup):
            lst = indexTable[a[i:i+ktup]]
            lst.append(i)
            indexTable[a[i:i+ktup]] = lst
        return indexTable

    # Gets the matches of substrings (length ktup) between the two sequences
    def getMatches(indexTable, b, ktup):
        matches = []
        for i in range(0, len(b) + 1 - ktup):
            bsubString = b[i:i+ktup]
            aMatchPositions = indexTable[bsubString]
            for position in aMatchPositions:
                matches.append([position, i])
        return matches

    def orderPairs(matches, a, b):
        diagonalPairs = {}
        for x in range(-len(a), len(b) + 1):
            diagonalPairs[x] = []
        for match in matches:
            lst = diagonalPairs[(match[1]-match[0])]
            lst.append(match)
            diagonalPairs[(match[1]-match[0])] = lst
        return diagonalPairs

    def scoreDiagonals(diagonalPairs, subMat, alphabet, a, b, ktup):
        diagonalScores = []
        for diagonalNum,diagonalValues in diagonalPairs.items():
            if(diagonalValues != []):  # i.e. some seed exists in the diagonal

                endPosition = -1
        
                # Loop through the diagonal values
                for diagonal in diagonalValues:

                    # Check if the diagonal have already been visited
                    if (diagonal[0] > endPosition):
                        
                        # Score the diagonal
                        diagonalScore, endPosition = scoreDiagonal(alphabet, subMat, a, b, diagonal[0], diagonal[1], ktup)
            
                        # Add the diagonal score
                        diagonalScores.append((diagonalNum, diagonalScore))
                        
        return diagonalScores

    def scoreDiagonal(alphabet, subMat, a, b, startA, startB, ktup):
        totalScore = 0
        currentPos = 0

        bestScore = 0
        bestPosition = 0
        
        visited = []
        while(startA + currentPos < len(a) and startB + currentPos < len(b)):
            currentScore = subMat[alphabet.index(a[startA + currentPos])][alphabet.index(b[startB + currentPos])]
            if(totalScore + currentScore > totalScore):
                totalScore += currentScore
                bestScore = totalScore
                bestPosition = currentPos
                currentPos += 1
            elif(totalScore + currentScore > 0):
                totalScore += currentScore
                currentPos += 1
            else:
                break;
        return totalScore, startA + currentPos

    def evaluateBestDiagonals(diagonalScores, subMat, alphabet, a, b, ktup, diagonalWidth):
        count = 0
        bestScore = 0
        bestAlignments = []
        while(count < 10 and bool(diagonalScores)):
            maxVal = max(diagonalScores,key=itemgetter(1))[0]
            results = dynprog(alphabet, subMat, a, b, maxVal, diagonalWidth)
            if(bestScore < results[0]):
                bestScore = results[0]
                bestAlignments = [results[1], results[2]]
            diagonalScores = [x for x in diagonalScores if x[0] != maxVal]
            count += 1
        return bestScore, bestAlignments





    # SMITH-WATERSON (local alignment of two strings)
    # LIMITED to only part of the matrices

    def dynprog(alphabet, subMat, a, b, diagonal, diagonalWidth):
        lst = populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth)
        scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
        alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
        scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
        return scoreAndAlignment

    def populateScoringMatrix(alphabet, subMat, a, b, diagonal, diagonalWidth):
        maxValue = 0
        maxValuePosition = [0, 0]

        # Initialise matrices
        scoMat = initialiseScoringMatrix(alphabet, subMat, a, b)
        dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b)

        # Find starting positions
        # Note: The purpose of this part is to loop down the diagonal line and calculate all values
        #       in the +- area of that diagonal (determined by the diagonalWidth). 
        # Since we already calculated row 0, we start on row 1, in which the diagonal position would've incremented 1 (due to the nature of diagonals2)
        if(diagonal > 0):
            startX = 1; startY = diagonal + 1  
        # Since we need previous rows to calculate current ones, we start at the highest possible row we need to calculate (at minimum 1)
        # For each row up we go, we must decrement the centre of the diagonal (i.e. startY) by 1 
        elif(diagonal < 0):
            if(diagonal - diagonalWidth < 1):
                startX = 1
                startY = diagonal + startX
            else:
                startX = diagonal - diagonalWidth
                startY = 1 - diagonalWidth
        # Only other case involves starting at 1, 1 - since we already calculated the 0th row and column
        else:
            startX = 1; startY = 1

        # Loop through matrix until we are out of bounds
        while(startX  < len(a) + 1 and startY - diagonalWidth < len(b) + 1):
            
            # For each row, loop through values that could only be within diagonal restriction
            for diagonalPoint in range(startY - diagonalWidth, startY + diagonalWidth + 1):

                #Check if new y position is actually within the y range
                if(diagonalPoint >= 1 and diagonalPoint < len(b) + 1):

                    # Get the diagonal score
                    dia = scoMat[startX-1][diagonalPoint - 1] + subMat[alphabet.index(a[startX - 1])][alphabet.index(b[diagonalPoint - 1])]

                    # Get the left point (if possible)
                    if(scoMat[startX][diagonalPoint - 1] != ' '): 
                        left = scoMat[startX][diagonalPoint-1] + subMat[alphabet.index(b[diagonalPoint - 1])][len(alphabet)]
                    else:
                        left = False

                    # Get the up point (if possible)
                    if(scoMat[startX-1][diagonalPoint] != ' '): #up is available
                        up = scoMat[startX-1][diagonalPoint] + subMat[len(alphabet)][alphabet.index(a[startX - 1])]
                    else:
                        up = False

                    # Calculates the value for the backtracking matrix
                    if(up == False):
                        bestScore = max(dia, left, 0)
                        if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                        elif bestScore == left: dirMat[startX][diagonalPoint] = "L"
                    elif(left == False):
                        bestScore = max(dia, up, 0)
                        if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                        elif bestScore == up: dirMat[startX][diagonalPoint] = "U"
                    else:
                        bestScore = max(dia, left, up, 0)
                        if bestScore == dia: dirMat[startX][diagonalPoint] = "D"
                        elif bestScore == up: dirMat[startX][diagonalPoint] = "U"
                        elif bestScore == left: dirMat[startX][diagonalPoint] = "L"

                    # Updates the scoring matrix
                    scoMat[startX][diagonalPoint] = bestScore
                    
                    # Updates the best score value
                    if(bestScore > maxValue):
                        maxValue = bestScore; maxValuePosition[0] = startX; maxValuePosition[1] = diagonalPoint

            # Increment the values of which diagonal we are following
            startX += 1
            startY += 1
        return [scoMat, dirMat, maxValue, maxValuePosition]

    # Function simply initialises the scoring Matrix
    def initialiseScoringMatrix(alphabet, subMat, a, b):
        scoMat = np.zeros((len(a)+1, len(b)+1))
        scoMat[0][0] = 0
        for x in range(1, len(a) + 1):
            scoMat[x][0] = 0
        for y in range(1, len(b) + 1):
            scoMat[0][y] = 0
        return scoMat

    def initialiseDirectionMatrix(alphabet, subMat, a, b):
        dirMat = np.empty((len(a)+1, len(b)+1), dtype='U')
        for x in range(1, len(a) + 1):
            dirMat[x][0] = "U"
        for y in range(1, len(b) + 1):
            dirMat[0][y] = "L"
        return dirMat

    def getBestMatching(scoMat, dirMat, a, b, maxValuePos):
        xPos = maxValuePos[0]; yPos = maxValuePos[1]
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
        for mat in matrix:
            print(mat)  
    
    matches = []
    ktup = 2
    diagonalWidth = 16
    while(matches == []):
        ktup -= 1
        indexTable = initialiseIndexTable(a, ktup)
        matches = getMatches(indexTable, b, ktup)
    diagonalPairs = orderPairs(matches, a, b)
    diagonalScores = scoreDiagonals(diagonalPairs, subMat, alphabet, a, b, ktup)
    score, align = evaluateBestDiagonals(diagonalScores, subMat, alphabet, a, b, ktup, diagonalWidth)
    return [score, align[0], align[1]]



a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA")
print("Score:   ", a[0])
print("Indices: ", a[1],a[2])
b = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AACAAADAAAACAADAADAAA", "CDCDDD")
print("Score:   ", b[0])
print("Indices: ", b[1],b[2])
c = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD", "DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCDCDCD")
print("Score:   ", c[0])
print("Indices: ", c[1],c[2])