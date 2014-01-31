## @file Puzzle.py
# @author Mathew Anderson
# @brief Store a "puzzle" according to the project specifications
# Note that this class will also emit the current state of the puzzle.
# There is no difference between a Puzzle and a world state, and therefore
# a Puzzle may be queried for information concerning movement.

## The puzzle class allows queries at a given (col, row),
# is aware of how many wrigglers are on the board, and can
# be considered the world state.
# NOTE: All col, row references are ZERO based
class Puzzle:

   ## Symbolic constant representing an empty square
   EMPTY_SQAURE = 'e'

   ## Ctor initializes all member vars to 0/empty
   def __init__(self):
      self.numCols = 0
      self.numRows = 0
      self.numWrigglers = 0
      self.puzzle = []

   ## Combine the row and col to get the index of the
   # specified tile in the list
   # @param col Desired column
   # @param row Desired row
   def GetLinearIndex(self, col, row):
      return (row * self.numCols) + col

   ## Given a (col, row) return the character
   # @param col The desired column
   # @param row The desired row
   def GetTile(self, col, row):
      linearIndex = self.GetLinearIndex(col, row)
      return self.puzzle[linearIndex]

   ## Given a col, row return if the space is "open"
   # @param col The desired column
   # @param row The desired row
   def IsOpen(self, col, row):
      linearIndex = self.GetLinearIndex(col, row)
      openTile = self.puzzle[linearIndex] == Puzzle.EMPTY_SQAURE
      return openTile

   ## Print the current world state consistent with
   # the project specifications.
   def PrintPuzzle(self):
      tileIndex = 1
      stringRep = ''
      for tile in self.puzzle:
         stringRep += tile
         if tileIndex % self.numCols == 0 and tileIndex != len(self.puzzle):
            stringRep += '\n'
         else:
            stringRep +=  ' '
         tileIndex += 1
      print stringRep

   ## @var numCols
   # Total number of columns (width) of the puzzle

   ## @var numRows
   # Total number of rows (height) of the puzzle

   ## @var numWrigglers
   # Total number of wrigglers in the puzzle

   ## @var puzzle
   # Linear representation of the puzzle

if __name__ == "__main__":
   puz = Puzzle()
   puz.numCols = 3
   puz.numRows = 3
   puz.numWrigglers = 1
   puz.puzzle = ['e', 'e', 'x', 'e', 'x', 'e', '0', '<', 'L']

   puz.PrintPuzzle()

   print "Testing IsOpen on " + puz.GetTile(0,2)
   if puz.IsOpen(0, 2):
      print "FAILED is open O, 2!"
   else:
      print "PASSED is open 0, 2 (it is not)"

   print "Testing IsOpen on " + puz.GetTile(0,1)
   if puz.IsOpen(0, 1):
      print "Passed basic IsOpen(0,1) (it is open)"
   else:
      print "FAILED basic IsOpen (0, 1)"

   print "Testing IsOpen on " + puz.GetTile(1,1)
   if puz.IsOpen(1,1):
      print "Failed IsOpen on wall"
   else:
      print "Passed IsOpen on wall (it is not open)"
