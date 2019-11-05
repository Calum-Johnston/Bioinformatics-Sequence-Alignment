# Hirschberg's Algorithm
# https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm

def dynproglin(alphabet, subMat, a, b):

    if(len(a) <= 1 or len(b) <= 1):
        print("s")

    for i in range(0, len(a)):
        print("Hio")
    


#Examples 
#a = [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]]
#dynproglin("ABC", a, "ABCACA", "BAACB")

#b = [[1,-1,-1,-1,-2],[-1,1,-1,-1,-2],[-1,-1,1,-1,-2],[-1,-1,-1,1,-2],[-2,-2,-2,-2,1]]
#dynproglin("ACGT", b, "AAAC", "AAGC") 

#c = [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]]
#dynproglin("ACGT", c, "GACTTAC", "CGTGAATTCAT") 