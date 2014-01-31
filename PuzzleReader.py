## @file PuzzleReader.py
# @author Mathew Anderson
# @brief Reads in puzzle file given a filename.
# The reader will generate a world state or Puzzle instance

from Puzzle import Puzzle

## Given a file name, generate a Puzzle class and return it or, upon error
# return None
# @param filename The name of the file to parse as a puzzle
# @note Assumed puzzle format is:
# <num cols> <num rows> <num wrigglers>
# <0,0> <1,0> ... <num cols - 1, 0>
# <0,1> <1,1> ... <num cols - 1, 1>
# ...
# <0, num rows - 1> <1, num rows-11> ... <num cols -1, num rows -1>
def ReadPuzzle(filename):
   puzFile = open(filename, 'r')

   initialPuzzle = None
   # Read the header line
   headerLine = puzFile.readline()

   # try to split the header line and assure three tokens
   headerTokens = headerLine.split()
   if len(headerTokens) == 3:
      try:
         # initialie the puzzle return value
         initialPuzzle = Puzzle()

         # first number is column count
         initialPuzzle.numCols = int(headerTokens[0])
         # second number is row count
         initialPuzzle.numRows = int(headerTokens[1])
         # final number is wriggler count
         initialPuzzle.numWrigglers = int(headerTokens[2])

      except Exception as e:
         # If any number parsing fails, just carry on.
         # We'll return the None puzzle indicating failure
         print "FAILED to parse puzzle in " + filename
         print "Exception says " + e.message
         print "Confirm formatting."
         return None

   # Now that we have the number of rows, we can start reading
   # in puzzle lines
   currPuzzleLine = 1
   for nextLine in puzFile:
      if currPuzzleLine <= initialPuzzle.numRows:
         # split the line into tile tokens
         tiles = nextLine.split()
         # and append the tiles onto the initial puzzle
         initialPuzzle.puzzle += tiles

      else:
         print "FAILED to parse puzzle in " + filename
         print "Tried to parse " + str (currPuzzleLine) \
            + " but there are only " + str(initialPuzzle.numRows) \
            + " according to the header!"
         del initialPuzzle
         initialPuzzle = None

   return initialPuzzle

if __name__ == "__main__":
   puzzleFile = raw_input ('Enter puzzle filename: ')
   thePuzz = ReadPuzzle(puzzleFile)
   print thePuzz.puzzle
   print "Has length " + str(len(thePuzz.puzzle))
