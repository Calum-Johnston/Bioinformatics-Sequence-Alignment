# FASTA algorithm (Heuristic)
import itertools

def heuralign(alphabet, subMat, a, b, ktup):
    indexTable = initialiseIndexTable(alphabet, a, ktup)
    matches = getMatches(indexTable, a, b, ktup)

def initialiseIndexTable(alphabet, a, ktup):
    keywords = [''.join(i) for i in itertools.product("ABCD", repeat = 2)]
    indexTable = {}
    for keyword in keywords:
        indexTable[keyword] = []
    for i in range(0, len(a) + 1 - ktup):
        indexTable[a[i:i+ktup]] = indexTable[a[i:i+ktup]] + [i]
    return indexTable

def getMatches(indexTable, a, b, ktup):
    matches = []
    for i in range(0, len(b) + 1 - ktup):
        bsubString = b[i:i+ktup]
        aMatchPositions = indexTable[bsubString]
        for position in aMatchPositions:
            matches.append([position, i])
    return matches


a = heuralign ("ABCD", [[1,-5,-5,-5,-1],[-5, 1,-5,-5,-1],[-5,-5, 5,-5,-4],[-5,-5,-5, 6,-4],[-1,-1,-4,-4,-9]], "AAAAACCDDCCDDAAAAACC", "CCAAADDAAAACCAAADDCCAAAA", 2)
#print("Score:   ", a[0])
#print("Indices: ", a[1],a[2])