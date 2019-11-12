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

    for j in range(0, len(b)):
        scoringMatrix[0][j] = Sc

    for i in range(0, len(a)):
        for j in range(0, len(b)):
            
            # Account for the first row


def printMatrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])

def reverseList(lst):
    return lst[::-1]

    


    

NWScore("asdasa", "asfa")

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