#*--------------------------------------------------------------------*#
#* We take a solved Sudoku 9 by 9 grid, permutes the rows 	          *#
#* and column a set number of times then mask a % of cells to reveal  *#
#* an unsolved Sudoku grid. Note: It has been conjectured that        *#
#* a standard puzzle need only have 17 clues for the solution to be   *#
#* unique - see http://arxiv.org/abs/1201.0749 for further details    *#
#*We use OO principles in the code design.                            *#
#*--------------------------------------------------------------------*#
#*--------------------------------------------------------------------*#
#Constraints:

#- 1. The numbers in the squares in any row must be each of 1 to 9
#- 2. The values in the squares in any column must be each of 1 to 9
#- 3. The values in the squares in any box must be each of 1 to 9 (a box is one of the 9 non-overlapping 3x3 grids within the overall 9x9 grid)
#- 4. There must be only one number within any square 
#- 5. The starting sudoku numbers must be in those same places in the final solution. Naturally 
#     if we have a lot of missing values in the grid, we would expect a larger number of  
#     feasible solutions.



#allows reference to the random class libraries
import random
import numpy as np
import cvxpy as cp
import cvxopt
import time

class Sudokugrid:

    #this is the class constructor
    def __init__ (self,maskpct=0.3,MC=100):

        #Enter a solved Sudoku rows*columns grid (9 * 9)
        #self.solvedGrid=[[0 for i in range(columns)] for i in range(rows)]
        self.solvedGrid =  [
                   [1,2,4,6,7,9,5,8,3]
                  ,[6,5,7,8,3,4,1,2,9]
                  ,[3,8,9,2,1,5,6,7,4]
                  ,[2,4,3,1,6,8,9,5,7]
                  ,[5,7,6,9,2,3,8,4,1]
                  ,[8,9,1,5,4,7,3,6,2]
                  ,[7,1,8,4,9,6,2,3,5]
                  ,[9,3,5,7,8,2,4,1,6]
                  ,[4,6,2,3,5,1,7,9,8]
                      ]
        
        self.NumRows = len(self.solvedGrid)
        self.NumColumns = self.NumRows

        self.getFinalSudokuGrid(maskpct,MC)


                                                                                                                                                                                                                                                                       
    def swapRows(self,rw1,rw2):
        "function to swap two rows"
        #rw1: is the first row to swap
        #rw2: is the second row to swap

        for c in range(len(self.solvedGrid)):
            temp=self.solvedGrid[rw1][c]
            self.solvedGrid[rw1][c]=self.solvedGrid[rw2][c]
            self.solvedGrid[rw2][c]=temp
            

    def swapColumns(self,cl1,cl2):
        "function to swap two columns"
        #cl1: is the first row to swap
        #cl2: is the second row to swap

        for r in range(len(self.solvedGrid)):
            temp=self.solvedGrid[r][cl1]
            self.solvedGrid[r][cl1]=self.solvedGrid[r][cl2]
            self.solvedGrid[r][cl2]=temp

    @property
    def grid(self):
        "return the current instance of the solved grid"
        return self.solvedGrid
                    
    @grid.setter
    def grid(self,x):
        "sets the current instance of the solved grid"
        self.solvedGrid = x
    
    @staticmethod
    def print_sudoku(x):
        print("-"*37)
        for i, row in enumerate(x):
            print(("|" + " {}   {}   {} |"*3).format(*[x if x != None else " " for x in row]))
            if i == 8:
                print("-"*37)
            elif i % 3 == 2:
                print("|" + "---+"*8 + "---|")
            else:
                print("|" + "   +"*8 + "   |")

    def permuteArray(self,MC=1000):
        "function to permute the rows and columns of an array"
        #MC     : is the number of Monte Carlo simulations

        MCIndex=1
        while (MCIndex<=MC):
            #choose two random columns that are different. Since we only want to select random columns within the 3 by 3 block grid  
            rndBox=random.randint(1, 3)
            rndCol1=(rndBox-1)*3+random.randint(1, 3)-1
            rndCol2=(rndBox-1)*3+random.randint(1, 3)-1
           

            while (rndCol1==rndCol2):
                rndCol2=(rndBox-1)*3+random.randint(1, 3)-1
           

            #choose two random rows that are different. Since we only want to select random rows within the 3 by 3 block grid   
            rndBox=random.randint(1, 3)
            rndRow1=(rndBox-1)*3+random.randint(1, 3)-1
            rndRow2=(rndBox-1)*3+random.randint(1, 3)-1
            while (rndRow1==rndRow2):
                rndRow2=(rndBox-1)*3+random.randint(1, 3)-1

            #print (rndCol1," ",rndCol2)
            #print (rndRow1," ",rndRow2)
          
         
            self.swapColumns(rndCol1,rndCol2)
            
            self.swapRows(rndRow1,rndRow2)
            #print ("MC=",MCIndex,MC)
            MCIndex=MCIndex+1

       
    def getFinalSudokuGrid(self,maskpct=0.5,MC=100):
        "function to output the final NumRows*NumColumns Sudoku grid"                                                                                                                         
        #maskpct       : is a percent from 0-100% - the default is set to 50%                                                                                 
        #MC         : is the number of Monte carlo row and column permutations of the original base grid                                                   
                                                                                                                                                          
                                                                                                                                                            
        #permute the columns and rows MC number of times
        self.permuteArray(MC)                                                                                                                   

        #create an array to hold the row, column, and random number for each cell of the rows*columns Sudoku grid                                                                                                                                     
        rndArray=[[0 for i in range(self.NumColumns)] for i in range(self.NumRows**2)]
        index=0
        #simple random sampling routine (without replacement)                                                                                        
        for rw in range(self.NumRows):
            for cl in range(self.NumColumns):
                rndArray[index][0]=rw
                rndArray[index][1]=cl
                rndArray[index][2]=random.random()
                #print(index,rw,cl,rndArray[index][2])
                index=index+1
               

        #sort the array in decending order (using the probabilities)                                                                                                                                               
        rndArray.sort(key=lambda a:a[2],reverse=True)                                                                                                                                                   
                                                                                                                                    
        #get the number of random cells to mask on the 9*9 grid based on the difficulty level                                                                       
        maskNum=round(self.NumRows**2*maskpct)                                                                                                              

        index=0
        while (index<maskNum):
            rndRow=rndArray[index][0]
            rndCol=rndArray[index][1]
            self.solvedGrid[rndRow][rndCol]=None
            index=index+1

    @staticmethod       
    def check_sudoku_valid(x):
        "function to check wheather a fully populated Sudoku grid x is valid"                                                                                                                         
        #get the size of the grid 
        value = len(x)
        #check to see if there are any missing cells.
        if np.sum(np.array(x)==None)>0:
            return False

        for row in x:
            #check that len(row) == len(x)
            # so we know we have a square
            if len(row) != len(x):
                return False
        for row in x:
            # For each element l in each row of x
            # check that it's not greater
            # than len(x) and also that thing is
            # not a float.
            for l in row:
                if l>len(x):
                    return False
                elif isinstance(l,float) or l<1:
                    return False
        # Loop through value at increments of -1
        # checking that l does not occur more
        # than once per row
        while value>0:
            for row in x:
                for l in row:
                    if row.count(l) > 1:
                        return False;
                    else:
                        value-=1
        # Check for recurrences per column
        value = len(x)
        eachRow = []
        # While value is greater than 0, cycle through
        # each row of x, appending whatever is at
        # row[value-1] to the list eachRow.
        # Check that l does not occur more than once
        # per column and that l is not a float.
        while value>0:
            for row in x:
                eachRow.append(row[value-1])
            for l in eachRow:
                if l > len(x):
                    return False
                elif eachRow.count(l) > 1:
                    return False
                elif isinstance(l,float) or l<1:
                    return False
                else:
                    eachRow = []
                    value-=1
            return True


    @staticmethod 
    def isPossible(x, row, col, val):
        #check to see if the added value is possible on the grid x
        for j in range(0, 9):
            if x[row][j] == val:
                return False

        for i in range(0, 9):
            if x[i][col] == val:
                return False

        startRow = (row // 3) * 3
        startCol = (col // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if x[startRow+i][startCol+j] == val:
                    return False
        return True
    
    @staticmethod 
    def solve_sudoku(x):
        #solve Sudoku using backtracking (recursion) on the grid x
        #loop through each row 
        for _row in range(0, 9):
            #loop through each column
            for _col in range(0, 9):
                #check to see if we have a missing cell
                if x[_row][_col] == None:
                    #check each of the possible 1-9 values for the missing cell
                    for val in range(1, 10):
                        #if value is a possible match replace the missing value with it
                        if Sudokugrid.isPossible(x,_row, _col, val):
                            x[_row][_col] = val
                            #recursively call again with the current version of the grid
                            Sudokugrid.solve_sudoku(x)

                            # Bad choice, make it blank and check again
                            #x[_row][_col] = 0
                    return x
                

def cvxpy_sudoku(grid):
    #solve Sudoku using cvxpy integer optimisation with the input grid

    #set to integer optimisation
    x = cp.Variable((9, 9), integer=True)

    # any objective function will do here as we only have to satisfy the constraints
    objective = cp.Minimize(cp.sum(x))
    identity = cvxopt.matrix(np.eye(9))

    constraints = []

    constraints += [x >= 1,  # all values should be >= 1
    x <= 9,  # all values should be <= 9
    cp.sum(x, axis=0) == 45,  # sum of all rows should be 45
    cp.sum(x, axis=1) == 45,  # sum of all cols should be 45
    ]

    #ensure each 3*3 block sum to 45
    for i in range(3):
        for j in range(3):
            constraints += [cp.sum(x[(3*i):(3*(i+1)), (3*j):(3*(j+1))]) == 45]

    #find location of the filled values on the grid (row,column,value) format
    out = np.where(grid!=None)
    #loop over the valid cases and put them as additional constraints
    valid_cases = out[0].shape[0]
    for i in range(valid_cases):
        row_index = out[0][i]
        col_index = out[1][i]
        #print([row_index,col_index,out_array[row_index,col_index]])
        constraints += [x[row_index, col_index] == grid[row_index,col_index]]

    prob = cp.Problem(objective, constraints)
    prob.solve()

    return x.value
                                                                                                                                           
if __name__ == '__main__':
    #Create Sudoku instance with %masking
    sud_instance=Sudokugrid(maskpct=0.2,MC=10000)
    #get the masked grid that needs to be solved
    x = sud_instance.grid
    print("Unsolved Sudoku grid: \n")
    sud_instance.print_sudoku(x)


    #-- Solve using backtracking
    start_backtracking = time.time()
    solved_grid = sud_instance.solve_sudoku(x)
    print("Solved Sudoku grid (backtracking): \n")
    sud_instance.print_sudoku(solved_grid)
    print("Is valid solution (backtracking): ",sud_instance.check_sudoku_valid(solved_grid))
    end_backtracking = time.time()
    print("Execution time of Sudoku backtracking solver (seconds): ",np.round(end_backtracking-start_backtracking,2))

    print("\n\n")

    #-- Solve using cvxpy optimisation framework
    start_cvxpy = time.time()

    solved_grid_cvxpy = cvxpy_sudoku(np.array(x))
    if solved_grid_cvxpy is not None:
        print("Solved Sudoku grid (cvxpy optimisation framework): \n")
        sud_instance.print_sudoku(solved_grid_cvxpy.astype(int).tolist())
        print("Is valid solution (cvxpy optimisation framework): ",sud_instance.check_sudoku_valid(solved_grid_cvxpy.astype(int).tolist()))
        end_cvxpy = time.time()
        print("Execution time of Sudoku solver using cvxpy optimisation framework (seconds): ",np.round(end_cvxpy-start_cvxpy,2))

    else:
        print("Unable to solve using cvxpy optimisation")