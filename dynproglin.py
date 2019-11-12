# Hirschberg's Algorithm
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm

def dynproglin(alphabet, subMat, a, b):

    def Hirschberg(a, b, alphabet, subMat):
        aAlign, bAlign = "", ""
    
        if(len(a) == 0):
          for i in range(0, len(b)):
                aAlign += a[i]
                bAlign += "-"
        elif(len(b) == 0):
            for i in range(0, len(a)):
                aAlign + "-"
                bAlign += b[i]
        elif(len(a) == 1 and len(b) == 1):
            #Perform normal dynprog on it (NeedelanWunsch)
            print("hi")
        else:
            aMid = int(len(a) / 2)
            scoreL = NWScore(a[:aMid], b, alphabet, subMat)
            scoreR = NWScore(reverseList(a[aMid:]), reverseList(b), alphabet, subMat)

            temp = scoreL + reverseList(scoreR)
            bMid = temp.index(max(temp))

            aAlign_l, bAlign_1 = Hirschberg(a[:aMid], b[:bMid], alphabet, subMat)
            aAlign_r, bAlign_r = Hirschberg(a[aMid:], b[bMid:], alphabet, subMat)

            aAlign = aAlign_l + aAlign_r
            bAlign = bAlign_1 + bAlign_r

        return aAlign, bAlign



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


def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

def reverseList(lst):
    return lst[::-1]

    


    

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