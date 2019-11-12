# Bioinformatics-Sequence-Alignment
An implementation of a variety of algorithms designed to identify global and local alignments of two sequences

Global Alignment:
- Needleman Wunsch Algorithm 
- Hirschberg's Algorithm

Local Alignment:
- Smith-Waterson Algorithm



### FORMAT
INPUT: (Alphabet, Substitution Matrix, sequence_1, sequence_2) where
- Alphabet is a string
- Substitution Matrix is a list of lists (2D array)
- Sequence 1 is a string
- Sequence 2 is a string

EXAMPLE:  
Alphabet could be "ABC"  
Substitution matrix:  
  	A 	B 	C 	_  
A 	1 	-1 	-2 	-1  
B 	-1 	2 	-4 	-1  
C 	-2 	-4 	3 	-2  
_ 	-1 	-1 	-2 	0

Sequence 1: ABCACA  
Sequence 2: BAACB
