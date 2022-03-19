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

class Sudokugrid:

    #this is the class constructor
    def __init__ (self,rows,columns,diff=0.3,MC=100):
        self.NumRows=rows
        self.NumColumns=columns
        #Enter a solved Sudoku rows*columns grid
        self.solvedGrid=[[0 for i in range(columns)] for i in range(rows)]
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
        self.getFinalSudokuGrid(diff,MC)
                                                                                                                                                                                                                                                                       
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


    def printArray(self):
        "function to print array contents"
        #myArray: is the data array to swap
            
        for r in range(len(self.solvedGrid)):
            print(self.solvedGrid[r])
                    
     
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

       
    def getFinalSudokuGrid(self,diff=0.5,MC=100):
        "function to output the final NumRows*NumColumns Sudoku grid"                                                                                                                         
        #diff       : is a percent from 0-100% - the default is set to 50%                                                                                 
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
        maskNum=round(self.NumRows**2*diff)                                                                                                              

        index=0
        while (index<maskNum):
            rndRow=rndArray[index][0]
            rndCol=rndArray[index][1]
            self.solvedGrid[rndRow][rndCol]=None
            index=index+1
            
                                                                                                                                             

if __name__ == '__main__':

    #print the result of the final permuted grid by creating a Sudoku grid
    Sud1=Sudokugrid(9,9,diff=0.2,MC=10000)
    Sud1.printArray()
