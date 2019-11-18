# FASTA algorithm (Heuristic)
import itertools

def heuralign(alphabet, subMat, a, b, ktup):
    indexTable = initialiseIndexTable(alphabet, a, ktup)
    matches = getMatches(indexTable, a, b, ktup)
    orderPairs(matches, a, b)

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
    for key in diagonalPairs:
        print("{}: {}".format(key, diagonalPairs[key]))

#a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "ACDA", "AB", 2)
a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA", 2)
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])
