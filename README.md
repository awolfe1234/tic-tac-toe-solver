# tic-tac-toe-solver
Logic tic-tac-toe puzzle solver 

To run you must open the file solve_v1.py and edit the file paths for the board to be imported 


Board input file(n = size of board, 0 = empty, 2 = O, 1 = X): 
n
0101
0011
1100
1010



1. Constraint 1 Recall that the first constraint of binary puzzle is that no three neighbouring rows/columns havethe same value. If it appears that the value of two out of three adjacent cells in a row/column were known and identical, then the value of the one remaining undetermined cell can be trivially deduced, which is equal to the negation of the known values.  

2. Constraint 2 The second constraint states that the number of zeros and ones in every row and column must
be equal. Equivalently as binary vector, each row/column of a binary puzzle is balanced. Following such a
constraint, the deduction of cells with unknown values in a row or a column can be done when the number of
zeros/ones is equal to n/2 (see Fig. 4).


3. Constraint 3 The third constraint, that is no two rows/columns are equal, involves comparison of rows/columns
in a binary puzzle. This allows the deduction of some value in cells of a row/column in the case when uniqueness
can be guaranteed. Figure 5 illustrates an example when such a situation may occur.
