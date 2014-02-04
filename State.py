## @file State.py
# @author Mathew Anderson
# @brief Define a state suitable for Puzzle Project.

from Move import Move

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
