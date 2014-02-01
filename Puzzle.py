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
   EMPTY_SQUARE = 'e'

   ## Ctor initializes all member vars to 0/empty
   def __init__(self):
      self.numCols = 0
      self.numRows = 0
      self.numWrigglers = 0
      self.puzzle = []

   ## Clone an instance of a puzzle
   # @param other The source of the clone
   def CopyFrom(self, other):
      self.numCols = other.numCols
      self.numRows = other.numRows
      self.numWrigglers = other.numWrigglers
      self.puzzle = list(other.puzzle)

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

   ## Given a wriggler within the puzzle,
   # set all of it's segments to empty.
   # @param wriggler Tiles to clear
   def ClearWriggler(self, wriggler):
      # set the head, tail, and segment locations to EMPTY_SQUARE
      # XXX - tuple.unpack()?
      self.ClearTile(wriggler.head.pos[0], wriggler.head.pos[1])
      self.ClearTile(wriggler.tail.pos[0], wriggler.tail.pos[1])

      for segment in wriggler.segments:
         self.ClearTile(segment.pos[0], segment.pos[1])

   ## Given a col, row, set a tile to the EMPTY_SQUARE char
   # @param col The column of the tile to clear
   # @param row The row of the tile to clear
   def ClearTile(self, col, row):
      linearIndex = self.GetLinearIndex(col, row)
      self.puzzle[linearIndex] = Puzzle.EMPTY_SQUARE

   ## Put the character representation of wriggler into the puzzle
   # @param wriggler Wriggler to place
   def PlaceWriggler(self, wriggler):
      self.SetTile(wriggler.head.pos[0], \
                   wriggler.head.pos[1], \
                   wriggler.head.dirOfNext)
      
      self.SetTile(wriggler.tail.pos[0], \
                   wriggler.tail.pos[1], \
                   wriggler.tail.idNumber)

      for segment in wriggler.segments:
         self.SetTile(segment.pos[0], \
                      segment.pos[1], \
                      segment.dirOfNext)

   ## Given a col, row, and desired char, update the puzzle
   # @param col Column of tile to set
   # @param row Row of tile to set
   # @param char Desired character to set
   def SetTile(self, col, row, char):
      linearIndex = self.GetLinearIndex(col, row)
      self.puzzle[linearIndex] = str(char)

   ## Given a col, row return if the space is "open"
   # @param col The desired column
   # @param row The desired row
   def IsOpen(self, col, row):
      linearIndex = self.GetLinearIndex(col, row)
      openTile = self.puzzle[linearIndex] == Puzzle.EMPTY_SQUARE
      return openTile

   ## Determine if a position is within the bounds of the puzzle
   # @param col The desired column
   # @param row The desired row
   # @return True if so, false otherwise
   def PositionInBounds(self, col, row):
      colInBounds = col > -1 and col < self.numCols
      rowInBounds = row > -1 and row < self.numRows
      return colInBounds and rowInBounds

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

   ## Same as PrintPuzzle but works with operator str
   def __str__(self):
      tileIndex = 1
      stringRep = ''
      for tile in self.puzzle:
         stringRep += tile
         if tileIndex % self.numCols == 0 and tileIndex != len(self.puzzle):
            stringRep += '\n'
         else:
            stringRep +=  ' '
         tileIndex += 1
      return stringRep

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

# XXX - num wrigglers can be dropped - it's only really interesting to the parser
