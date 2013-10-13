## @file Puzzle.py
# @author Mathew Anderson
# @brief Store a "puzzle" according to the project specifications
# Note that this class will also emit the current state of the puzzle.
# There is no difference between a Puzzle and a world state, and therefore
# a Puzzle may be queried for information concerning movement.

import hashlib

## The puzzle class allows queries at a given (col, row),
# is aware of how many wrigglers are on the board, and can
# be considered the world state.
# NOTE: All col, row references are ZERO based
class Puzzle:

   ## Symbolic constant representing an empty square
   EMPTY_SQUARE = 'e'
   ## Symbolic constant for wall square
   WALL_SQUARE = 'x'

   ## Ctor initializes all member vars to 0/empty
   def __init__(self):
      self.numCols = 0
      self.numRows = 0
      self.numWrigglers = 0
      self.puzzle = []
      self.hashValue = hashlib.new('sha1')

   ## Clone an instance of a puzzle
   # @param other The source of the clone
   def CopyFrom(self, other):
      self.numCols = other.numCols
      self.numRows = other.numRows
      self.numWrigglers = other.numWrigglers
      self.puzzle = list(other.puzzle)

   ## Add a line to the puzzle, incorporating its
   # contents into the hash value.
   # @param tiles The next puzzle tiles to add
   def AddLine(self, tiles):
      self.puzzle += tiles
      # convert the line into a string
      tileStr = ''.join(tiles)
      # add hash value
      self.hashValue.update(tileStr)

   ## Re-generate the hash associated with this puzzle object
   # used to incorporate a copy or move.
   def ReHashPuzzle(self):
      self.hashValue = hashlib.new('sha1')
      # change the puzzle tiles into one string
      # and hash it
      tileStr = ''.join(self.puzzle)
      self.hashValue.update(tileStr)

   ## Make any wriggler's body, etc an x
   def BlockOffWrigglers(self):
      newPuzzle = []
      for ch in self.puzzle:
         if ch.isdigit():
            newPuzzle.append('w')
         elif ch in ['<', '^', '>', 'v']:
            newPuzzle.append('w')
         elif ch in ['U', 'R', 'L', 'D']:
            newPuzzle.append('w')
         else:
            newPuzzle.append(ch)
      self.puzzle = newPuzzle

   ## Retrieve the stored hash value representing
   # this puzzle
   def GetPuzzleHash(self):
      return self.hashValue.hexdigest()

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

   ## Put a hash-able version of the wrigglers on the board
   # @param wriggler the wriggler to plae
   def PlaceWrigglerAllNumber(self,wriggler):
      self.SetTile(wriggler.head.pos[0], \
                   wriggler.head.pos[1], \
                   wriggler.tail.idNumber)
      
      self.SetTile(wriggler.tail.pos[0], \
                   wriggler.tail.pos[1], \
                   wriggler.tail.idNumber)

      for segment in wriggler.segments:
         self.SetTile(segment.pos[0], \
                      segment.pos[1], \
                      wriggler.tail.idNumber)

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

   ## Given a (col, row) position return if the space is "open"
   # @param position (col, row) position to check
   def IsOpen(self, position):
      linearIndex = self.GetLinearIndex(position[0], position[1])
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

   ## Determine if a position is within the bounds of the puzzle
   # @param position (col, row) to check
   # @return True if position is within bounds, false otherwise
   def PositionInBounds(self, position):
      colInBounds = position[0] > -1 and position[0] < self.numCols
      rowInBounds = position[1] > -1 and position[1] < self.numRows
      return colInBounds and rowInBounds

   ## Return a (col, row) that defines the "lower right"
   # corner of the puzzle.
   def GetLowerRightCornerPosition(self):
      return (self.numCols - 1, self.numRows - 1)

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

   ## @var hashValue
   # A sha-1 hash used to identify this puzzle.

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
