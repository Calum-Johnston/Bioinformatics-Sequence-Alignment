def dynproglin(alphabet, subMat, a, b):
    if(len(b) == 1):
        #align a[1..len(a)] and b[1,1]
        print(a)
    else:




#Examples 
#a = [[1,-1,-2,-1],[-1,2,-4,-1],[-2,-4,3,-2],[-1,-1,-2,0]]
#dynproglin("ABC", a, "ABCACA", "BAACB")

#b = [[1,-1,-1,-1,-2],[-1,1,-1,-1,-2],[-1,-1,1,-1,-2],[-1,-1,-1,1,-2],[-2,-2,-2,-2,1]]
#dynproglin("ACGT", b, "AAAC", "AAGC") 

#c = [[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]]
#dynproglin("ACGT", c, "GACTTAC", "CGTGAATTCAT") 