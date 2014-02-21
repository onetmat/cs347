## @file State.py
# @author Mathew Anderson
# @brief Define a state suitable for Puzzle Project.

from Move import Move
from Bres import BresLine

from Puzzle import Puzzle

## The state class tracks the world state (puzzle)
# and the list of wrigglers.
class State:

   ## Constant array of possible moves.
   # Anytime the ACTIONS are determined, both the head
   # and the tail might be able to move Up, Down, Left, or Right
   POSSIBLE_MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

   ## Ctor stores initial conditions
   def __init__(self, puzzle, wrigglers):
      self.puzzle = puzzle
      self.wrigglers = wrigglers

      # determine, for the sake of convience, the index
      # of the blue wriggler.
      for index, wriggler in list(enumerate(self.wrigglers)):
         if wriggler.tail.idNumber == 0:
            self.indexOfBlue = index

      # Calculate the heuristic cost in play
      self.CalculateHeuristic()

   ## Determine if the head or tail of the blue wriggler
   # is located in the lower right corner of the puzzle.
   # This constitutes a check for goal state.
   def BlueWrigglerInLowerRightCorner(self):
      lowerRightCorner = self.puzzle.GetLowerRightCornerPosition()
      return self.wrigglers[self.indexOfBlue].HeadOrTailAtPos(lowerRightCorner)

   ## Generate all legal moves from all wrigglers in the state
   def Actions(self):
      legalMoves = []

      # foreach wriggler, generate all Moves
      # and extend the legalMoves list
      for wriggler in self.wrigglers:
         wrigglerMoves = self.WrigglerActions(wriggler)
         legalMoves.extend(wrigglerMoves)

      return legalMoves

   ## Generate all legal moves from a given wriggler
   # @param wriggler The wriggler which is being considered for moving
   def WrigglerActions(self, wriggler):
      # initialize the output
      wrigglerActions = []
      # get the head & tail pos of wriggler
      headPos = wriggler.GetHeadPosition()
      tailPos = wriggler.GetTailPosition()
      tailNum = wriggler.GetTailNumber() # tail number is part of the Move
      # for each possible move
      for pMove in State.POSSIBLE_MOVES:
         # generate a new position for both head and tail
         newHead = (headPos[0] + pMove[0], headPos[1] + pMove[1])
         # for both head and tail pos
         # and if it is within the boundaries of the puzzle
         # and it's open
         if self.puzzle.PositionInBounds(newHead) and self.puzzle.IsOpen(newHead):
            # add it to our list of wriggler actions possible
            headMove = Move(tailNum, Move.HEAD, newHead[0], newHead[1])
            wrigglerActions.append(headMove)

         newTail = (tailPos[0] + pMove[0], tailPos[1] + pMove[1])

         if self.puzzle.PositionInBounds(newTail) and self.puzzle.IsOpen(newTail):
            tailMove = Move(tailNum, Move.TAIL, newTail[0], newTail[1])
            wrigglerActions.append(tailMove)

      # return the list of legal actions
      return wrigglerActions

   ## Return the stored heuristic cost of this state.
   def GetHeuristicCost(self):
      return self.heuristic

   ## Calculate the heuristic cost for this State.
   # @param which Variable for expansion later
   #    will ultimately allow heuristic selection
   def CalculateHeuristic(self):
      # Get goal position
      lowerRightCorner = self.puzzle.GetLowerRightCornerPosition()
      # get head position of blue wriggler
      headPos = self.wrigglers[self.indexOfBlue].GetHeadPosition()
      # get tail position of blue wriggler
      tailPos = self.wrigglers[self.indexOfBlue].GetTailPosition()


      ## Manhattan distance is almost never used in the max
      totSq = min( \
         self.GetTotalSquaresBetween(headPos, lowerRightCorner), \
         self.GetTotalSquaresBetween(tailPos, lowerRightCorner))       

      ## Can't really tell if this is dominant
      costOfMove = min( \
         self.GetCostOfMovement(headPos, lowerRightCorner), \
         self.GetCostOfMovement(tailPos, lowerRightCorner))

      ## Almost never correct
      bresLine = min( \
         len(BresLine(headPos, lowerRightCorner)) - 1, \
         len(BresLine(tailPos, lowerRightCorner)) - 1)

      ## This actually returns a max on some occaisons
      simpleDigestBresLine = min( \
         self.SimpleDigestBresLines(headPos, lowerRightCorner),
         self.SimpleDigestBresLines(tailPos, lowerRightCorner))

      totCostBresLine = min (\
         self.DigestBresLines(headPos, lowerRightCorner),
         self.DigestBresLines(tailPos, lowerRightCorner))

      # Euclidean distance is dominated by bres line
      #euclidDistance = min (\
         #self.EuclideanDistance(headPos, lowerRightCorner),
         #self.EuclideanDistance(tailPos, lowerRightCorner))

      #print "All heuristic costs: " +\
         #str([totSq, costOfMove, bresLine, simpleDigestBresLine, totCostBresLine])
      self.heuristic = max(totSq, costOfMove, bresLine, simpleDigestBresLine, totCostBresLine)

   def EuclideanDistance(self, start, end):
      dx = end[1] - start[1]
      dy = end[0] - start[0]

      return (dx ** 2 + dy ** 2) ** 0.5

   def GetDirectPuzzleString(self):
      return ''.join(self.puzzle.puzzle)

   def GetContinuousString(self):
      puzz = Puzzle()
      puzz.CopyFrom(self.puzzle)

      puzz.BlockOffWrigglers()
      # replace all wrigglers with just their number
      for wrig in self.wrigglers:
         puzz.PlaceWrigglerAllNumber(wrig)
      # make the entire thing on string
      # and return it
      contStr = ''.join(puzz.puzzle)
      return contStr

   def DigestBresLines(self, start, end):
      # Get a line from start to end
      line = BresLine(start, end)

      # Now, do a get cost of movement between every two points
      # to get sort of divide and conquer the true path
      totHeuristic = 0
      for index in range(0, len(line) - 1):
         totHeuristic += self.GetCostOfMovement(line[index], line[index+1])

      return totHeuristic

   ## Look at the tile in the puzzle.
   # If it's a wriggler body segment, the cost is 3
   # if it's a wall or wriggler head/tail cost is two
   # if it's open, cost is 1
   def GetRelaxedCostOfNode(self, pos):
      tileHCost = 0
      if self.puzzle.PositionInBounds(pos):
         if self.puzzle.IsOpen(pos):
            lnCost = 1
         elif self.puzzle.GetTile(pos[0], pos[1]) in ['^', 'v', '<', '>']:
            lnCost = 3
         else:
            lnCost = 2
         
      return tileHCost
         
   def SimpleDigestBresLines(self, start, end):
      lnCost = 0
      line = BresLine(start, end)
      del line[0] # it always has first point in there
      for tile in line:
         lnCost += self.GetRelaxedCostOfNode(tile)
      return lnCost
            

   ## Return the 2D Euclidean distance between two nodes.
   # @param start (col, row) of start tile
   # @param end (col, row) of end tile
   # Avoids taking square root for speed
   def GetTotalSquaresBetween(self, start, end):
      colsToGo = abs(start[0] - end[0])
      rowsToGo = abs(start[1] - end[1])

      return (colsToGo + rowsToGo)

   def GetCostOfMovement(self, start, end):
      colCostOfMovement = 0
      colCostOfMovement += self.ScanCol(start, end[1])
      colCostOfMovement += self.ScanRow((start[0], end[1]), end[0])
      rowCostOfMovement = 0
      rowCostOfMovement += self.ScanRow(start, end[0])
      rowCostOfMovement += self.ScanCol((end[0], start[1]), end[1])
      return min(colCostOfMovement, rowCostOfMovement)

   ## Scan a row for heuristic movement costs. Empty sqauare = 1
   # blocked counts for two (blocked == not empty).
   # @param startPos The (col, row) position from which the scan
   # should start
   # @param colCount Zero-based end of column
   # @return The total cost of moving along this row
   def ScanRow(self, startPos, colCount):
      rowCost = 0
      (currCol, row) = startPos
      currCol += 1
      while currCol <= colCount:
         rowCost += self.GetRelaxedCostOfNode((currCol, row))
         currCol += 1
      return rowCost

   ## Scan a col for heuristic movement costs. Empty sqauare = 1
   # blocked counts for two (blocked == not empty).
   # @param startPos The (col, row) position from which the scan
   # should start
   # @param rowCount Zero-based end of rows
   # @return The total cost of moving along this column
   def ScanCol(self, startPos, rowCount):
      colCost = 0
      (col, currRow) = startPos
      currRow += 1
      while currRow <= rowCount:
         colCost += self.GetRelaxedCostOfNode((col, currRow))
         currRow += 1
      return colCost

   ## Have each wriggler update it's character representation
   # and put that in the puzzle string itself.
   # Return the string representation of this action
   def ConstructSolution(self):
      return str(self)

   ## Return a representation of the puzzle with all wrigglers
   # placed.
   def __str__(self):
      for wrig in self.wrigglers:
         numSegs = len(wrig.segments)
         if numSegs > 0:
            wrig.head.UpdateSegmentCharacter(wrig.segments[0])
            for seg in xrange(0, numSegs-1):
               wrig.segments[seg].UpdateSegmentCharacter(\
                  wrig.segments[seg+1])

            wrig.segments[-1].UpdateSegmentCharacter(wrig.tail)
         else:
            wrig.head.UpdateSegmentCharacter(wrig.tail)

         self.puzzle.PlaceWriggler(wrig)
      
      return str(self.puzzle)

   ## @var puzzle
   # An object with rows and columns that defines an open
   # and closed state of each (col, row) tuple. This object
   # must also have a defniition for lower right corner and
   # be able to bounds check a given (col, row).

   ## @var wrigglers
   # A list of Wriggler objects
   # A Wriggler must have a head and tail and must allow
   # the state to present a (col, row) and determine if
   # the head or tail resides at that "position"

   ## @var heuristicCost
   # h(n) of this state.

if __name__ == "__main__":
   # test legal move determination
   from PuzzleReader import ReadPuzzle
   from WrigglerReader import FindWrigglers

   puzz = ReadPuzzle('puzz1.pz')
   wrigglers = FindWrigglers(puzz)
   state = State(puzz, wrigglers)

   allLegalMoves = state.Actions()

   for move in allLegalMoves:
      print str(move)
