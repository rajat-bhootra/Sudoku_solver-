import pycosat

#variable encoding:
def varnum(row, columns, digit):
    return 81*(row-1) + 9*(columns-1) + digit #Mapping cell (r,c) having digit d to a unique integer variable.

def exactly_one(literals, clauses):  #Enforces that exactly one literal in the given list is True.
    
    # At least one true:
    clauses.append(literals)
    
    # At most one true: for every pair add clause (-lit_i or -lit_j)
    # For every pair of literals, add a clause that prevents both from being True simultaneously.
    for i in range(len(literals)):
        for j in range(i+1, len(literals)):
            clauses.append([-literals[i], -literals[j]])

def sudoku_cnf():  #Returns : A list of clauses representing the CNF constraints for Sudoku.
    clauses = []

    # 1. Each cell has at least one value & at most one value.
    #    For each cell (row, column), generate a clause with 9 literals (one per digit),
    #    and then add pairwise constraints to ensure no cell gets more than one digit.
    for row in range(1, 10):
        for column in range(1, 10):
            lits = [varnum(row, column, digit) for digit in range(1, 10)]
            exactly_one(lits, clauses)

    # 2. Each row must contain each digit exactly once.
    #    For each row and for each digit, generate a clause that includes that digit
    #    in every column of the row, with additional pairwise constraints.
    for row in range(1, 10):
        for digit in range(1, 10):
            lits = [varnum(row, column, digit) for column in range(1, 10)]
            exactly_one(lits, clauses)

    # 3. Each column must contain each digit exactly once.
    #    For each column and for each digit, generate a clause that includes that digit
    #    in every row of the column, with additional pairwise constraints.
    for column in range(1, 10):
        for digit in range(1, 10):
            lits = [varnum(row, column, digit) for row in range(1, 10)]
            exactly_one(lits, clauses)

    # 4. Each 3x3 block must contain each digit exactly once.
    #    For each of the 9 blocks and for each digit, generate a clause with the cells in that block,
    #    ensuring that each digit appears exactly once in each block.
    for br in range(0, 3):                # Block row index (0,1,2)
        for bc in range(0, 3):            # Block column index (0,1,2)
            for digit in range(1, 10):
                lits = []
                # For each cell within the 3x3 block:
                for row in range(1 + 3*br, 1 + 3*br + 3):
                    for column in range(1 + 3*bc, 1 + 3*bc + 3):
                        lits.append(varnum(row, column, digit))
                exactly_one(lits, clauses)

    return clauses

def add_initial_clauses(clauses, puzzle):   # Returns : The updated list of CNF clauses including the initial clues.
    for i, ch in enumerate(puzzle):
        if ch in "123456789":
            # Compute row and column from index (1-indexed)
            r = i // 9 + 1
            c = i % 9 + 1
            d = int(ch)
            # Append a clause that fixes the cell at (r, c) to digit d.
            clauses.append([varnum(r, c, d)])
    return clauses
 
def solve_sudoku(puzzle):  #Returns: A string representing the solved Sudoku puzzle row-wise if a solution exists, or None.
    
    # Generate the general Sudoku CNF constraints.
    clauses = sudoku_cnf()
    
    # Add the initial clues from the puzzle to the CNF.
    clauses = add_initial_clauses(clauses, puzzle)
    
    # Use the SAT solver to find a solution.
    solution = pycosat.solve(clauses)
    
    # If the problem is unsatisfiable, return None
    if solution == "UNSAT":
        return None  # No solution exists

    # Create an empty 9x9 board
    board = [[0]*9 for _ in range(9)]
    
    # The solution from pycosat is a list of integers where a positive number means the corresponding variable is True.
    for var in solution:
        if var > 0:
            # Recover (row, colum, digtit) from variable number
            var = var - 1  # convert to 0-index for easier math
            d = var % 9 + 1
            var //= 9
            c = var % 9 + 1
            r = var // 9 + 1
            board[r-1][c-1] = d
            
    # Convert the 9x9 board to a single string by concatenating each row.
    return "".join("".join(str(cell) for cell in row) for row in board)

def main(): 
    puzzles = []
    
    file = input("enter the name of file: ")
    
    # Open the input file containing Sudoku puzzles.
    with open(file, "r") as file: #make sure that the file is there in current folder.
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace.
            if len(line) == 81:
                puzzles.append(line)

    solved_puzzles = []
    
    # Solve each puzzle in the list.
    for puzzle in puzzles:
        solution = solve_sudoku(puzzle)
        if solution:
            solved_puzzles.append(solution)
        else:
            solved_puzzles.append("No Solution\n")

    # Write all solutions to the output file.
    with open("solved.txt", "w") as file:
        for sol in solved_puzzles:
            file.write(sol + "\n")


# If this script is executed (rather than imported), run the main function.
if __name__ == "__main__":
    main()
