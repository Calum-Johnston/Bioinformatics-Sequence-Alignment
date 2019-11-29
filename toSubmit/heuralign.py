# FASTA algorithm (Heuristic)
import itertools

def heuralign(alphabet, subMat, a, b, ktup):
    indexTable = initialiseIndexTable(alphabet, a, ktup)
    matches = getMatches(indexTable, a, b, ktup)
    diagonalPairs = orderPairs(matches, a, b)
    scoreDiagonals(diagonalPairs, subMat, alphabet, a, b)

def initialiseIndexTable(alphabet, a, ktup):
    keywords = [''.join(i) for i in itertools.product("ABCD", repeat = 2)]
    indexTable = {}
    for keyword in keywords:
        indexTable[keyword] = []
    for i in range(0, len(a) + 1 - ktup):
        lst = indexTable[a[i:i+ktup]]
        lst.append(i)
        indexTable[a[i:i+ktup]] = lst
    return indexTable

def getMatches(indexTable, a, b, ktup):
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

def scoreDiagonals(diagonalPairs, subMat, alphabet, a, b):
    x,y = 0
    for diagonal,diagonalValues in diagonalPairs.items():
        print(diagonal)
        print(diagonalValues)
        if(diagonal > 0):
            x = 0
        currentAlign = []
        currentScore = 0
        bestAlign = []
        bestScore = 0
        #for dia in diagonals:
           # if(len(dia) != 0):  # Ignore diagonals with no matches
            #    score = subMat[alphabet.index(a[dia[0]])][alphabet.index(b[dia[1]])] + subMat[alphabet.index(a[dia[0] + 1])][alphabet.index(b[dia[1] + 1])]
                
            



# SMITH-WATERSON 
# Needs updating to limit matrix space used
def dynprog(alphabet, subMat, a, b, diagonalL, diagonalR):
    lst = populateScoringMatrix(alphabet, subMat, a, b, diagonalL, diagonalR)
    scoMat = lst[0]; dirMat = lst[1]; maxValue = lst[2]; maxValuePosition = lst[3]
    alignment = getBestMatching(scoMat, dirMat, a, b, maxValuePosition)
    scoreAndAlignment = [maxValue, alignment[0], alignment[1]]
    return scoreAndAlignment

def populateScoringMatrix(alphabet, subMat, a, b, diagonalX, diagonalY):
    scoMat = initialiseScoringMatrix(alphabet, subMat, a, b, diagonalX, diagonalY)
    dirMat = initialiseDirectionMatrix(alphabet, subMat, a, b, diagonalX, diagonalY)
    maxValue = 0
    maxValuePosition = [0, 0]
    currentX, currentY = 0
    while(currentX < len(a) + 1):
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

def initialiseScoringMatrix(alphabet, subMat, a, b, diagonalX, diagonalY):
    scoringMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    scoringMatrix[0][0] = 0
    for x in range(1, abs(diagonalX)):
        scoringMatrix[x][0] = max(0, scoringMatrix[x-1][0] + subMat[len(alphabet)][alphabet.index(a[x - 1])])   
    for y in range(1, diagonalY):
        scoringMatrix[0][y] = max(0, scoringMatrix[0][y-1] + subMat[len(alphabet)][alphabet.index(b[y - 1])])
    return scoringMatrix

def initialiseDirectionMatrix(alphabet, subMat, a, b, diagonalX, diagonalY):
    directionMatrix = [[' ' for x in range(len(b) + 1)] for y in range(len(a) + 1)]
    for x in range(1, abs(diagonalX)):
        directionMatrix[x][0] = "U"        
    for y in range(1, diagonalY):
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



#a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ABDAAB", "AB", 2)
a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC4", "CCAAADDAAAACCAAADDCCAAAA", 2)
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])
