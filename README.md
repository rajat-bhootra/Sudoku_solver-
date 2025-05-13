# Name - Rajat Bhootra
# Roll No. - 112301044

# Sudoku Solver using pycosat

This project implements a Sudoku solver by formulating a Sudoku puzzle as a Boolean satisfiability (SAT) problem. It encodes the puzzle into Conjunctive Normal Form (CNF) and uses the pycosat SAT solver to find a solution. The approach covers all the standard Sudoku constraints:

1. Each cell contains at least one value.
2. Each cell contains at most one value.
3. Each row contains all the values exactly once.
4. Each column contains all the values exactly once.
5. Each 3x3 block contains all the values exactly once.
6. The given initial setup is preserved.

## How It Works

- **Variable Encoding:**  
  Each variable represents the proposition "cell (r, c) contains digit d" where row, column, and digit range from 1 to 9. The mapping function is:  
              `varnum(r, c, d) = 81*(r-1) + 9*(c-1) + d`

- **Constraints Encoding:**  
  The Sudoku rules are transformed into CNF clauses. For example:
  - Every cell must have at least one digit.
  - No cell can have more than one digit (enforced using pairwise clauses).
  - Every row, column, and 3x3 block must contain every digit exactly once.

- **Solving:**  
  After encoding all constraints and the initial puzzle values (provided in an input file with 81 characters per puzzle, using `.` for empty cells), the CNF is passed to `pycosat.solve()`. The solution is then converted back to the 9×9 grid format.

## Installation

Ensure you have Python 3 installed on your system. You also need the `pycosat` package, which you can install by below commands:
(you can copy and paste these commands in terminal)

for windows : 
```bash
pip install pycosat
```

for linux :
```bash
sudo apt install pycosat
```

## How to run the code
unzip the 112301044.zip folder. before runnning the code make sure that the p.txt file is there.
now just run the python file sudoku_solver.py by using below command in terminal.(make sure you are in the 112301044 folder):
```bash
python3 sudoku_solver.py
```
enter the name of file you want to solve (in this case it is p.txt).
after successfully running the code you can see the solved sudokus in solved.txt in the folder.

## Detailed explantion of approach
1. Variable Encoding
Concept:
    We define a Boolean variable for every combination of cell and digit. Let X(r,c,d) be a variable that is true if and only if the cell in row r and column c contains the digit d.
Mapping:
    We have 9 rows, 9 columns, and 9 possible digits per cell, leading to a total of 9×9×9 = 729 variables.


A common mapping is:
                     `varnum(row,column,digit)=81×(row−1)+9×(column−1)+ digit`  

    This assigns a unique integer (from 1 to 729) to each variable, which is necessary for the SAT solver. 

2. Formulating Sudoku Constraints in CNF
Sudoku has several inherent constraints, and each is converted into Conjunctive Normal Form (CNF) clauses:

A. Cell Constraints
    At Least One Digit Per Cell:
        For each cell (r,c) we need at least one of the variables (Xr,c,1 ,Xr,c,2  ,… , Xr,c,9)​  to be true. 
        CNF Clause:
                    ( X(r,c,1) ∨ X(r,c,2) ∨ . . . ∨ X(r,c,9) )​ 

    At Most One Digit Per Cell:
        We must also ensure that no cell contains more than one digit. For every pair of distinct digits d and e (where d != e) in the same cell (r,c), we add:
        CNF Clause:
                    ( ¬(Xr,c,d) ∨ ¬X(r,c,e) )
        These pairwise clauses ensure that if one digit is chosen, the others are forced to be false.


B. Row Constraints
    Each row must have every digit exactly once.

    At Least One Occurrence in a Row:
        For each row r and digit d, ensure that the digit appears at least once in that row:
        CNF Clause:
                    ( (X(r,1,d) ∨ X(r,2,d) ∨ . . . ∨ X(r,9,d) )

    At Most One Occurrence in a Row:
        For any two different columns c and c' in the same row, add:
        CNF Clause:
                      ( ¬X(r,c,d) ∨ ¬X(r,c',d) )

C. Column Constraints
    Each column must also contain every digit exactly once.

    At Least One Occurrence in a Column:
        For each column c and digit d :
        CNF Clause:
                   ( X(1,c,d) ∨ X(2,c,d) ∨ . . . ∨ X(9,c,d) )

    At Most One Occurrence in a Column:
        For any two distinct rows r and r' :
        CNF Clause:
                    ( ¬X(r,c,d) ∨ ¬X(r',c,d) )

D. Block (3×3 Subgrid) Constraints
    Each of the nine 3×3 subgrids (blocks) must contain every digit exactly once.

    At Least One Occurrence in a Block:
        For each block, identified by block row br and block column bc (where br,bc∈{0,1,2}) and for each digit d, the clause is:
        CNF Clause:
                    ( X(r1,c1,d) ∨ X(r2,c2,d) ∨ . . . ∨ X(r9,c9,d) )

        Here, (ri,ci) are the coordinates of the cells in the block.


    At Most One Occurrence in a Block:
        For every pair of distinct cells within the block:
        CNF Clause:
                    ( ¬X(r,c,d) ∨ ¬X(r',c',d))

3. Incorporating the Initial Puzzle
The input puzzle is provided as a string of 81 characters (row-wise), where a digit represents a pre-filled cell and a period (.) represents an empty cell. For every pre-filled cell:
    Unit Clause:
    If cell (r,c) is pre-filled with digit d, we add the clause:
                    (X(r,c,d​))

This unit clause forces the SAT solver to assign that digit to the corresponding cell, preserving the initial puzzle configuration.

4. SAT Solving and Reconstruction
Once all constraints (cell, row, column, block, and initial conditions) are encoded as CNF clauses:

Solving:
    The CNF formula is given to `pycosat.solve()`, which either finds a satisfying assignment (if one exists) or returns "UNSAT" if the puzzle is unsolvable.

Decoding the Solution:
    The solver returns a list of integers representing the variables that are true. Each positive integer is mapped back to its corresponding (r,c,d) using the reverse of the initial mapping. The resulting assignments are then used to reconstruct the completed 9×9 Sudoku grid.

Output:
    The final solution is formatted as a single string of 81 digits (row-wise) that represents the solved puzzle.


This method leverages the efficiency of SAT solvers to handle the combinatorial constraints of Sudoku by reducing the problem to a Boolean SAT problem in CNF.