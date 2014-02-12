## @file WrigglerMover.py
# @author Mathew Anderson
# @brief Definition of routine that can move a wriggler on a puzzle

from Wriggler import Wriggler, HEAD_CHARS, SEGMENT_CHARS
from Puzzle import Puzzle
from Move import Move

## Bridges Wriggler, Move, and Puzzle.
# @param wriggler information about the wriggler being moved
# @param move Details concerning the move
# @param puzzle World state
# @returns (New Wriggler, New World)
# both of which reflecting the effect of the move
def MoveWriggler(wriggler, move, puzzle):
   newPuzzle = Puzzle()
   newWriggler = None
   try:
      # First, update the wriggler itself to get the correct characters
      # the update method returns a new wriggler
      newWriggler = UpdateWriggler(wriggler, move)
      # and now we can clear out the characters from the puzzle
      # update the puzzle with the new wriggler information
      newPuzzle.CopyFrom(puzzle)
      newPuzzle.ClearWriggler(wriggler)
      newPuzzle.PlaceWriggler(newWriggler)
      # update the hash value
      newPuzzle.ReHashPuzzle()

   except:
      raise

   return (newWriggler, newPuzzle)

## Given a wriggler and a move, update the positions
# and all character representations of the segments
# @param wriggler The wriggler to move
# @param Information about the move
# @return A new Wriggler instance that incorporates the move
# or None on error
def UpdateWriggler(wriggler, move):

   newWriggler = None
   # Given valid input
   try:
      if move.tailNumber == wriggler.tail.idNumber:
         newWriggler = Wriggler()

         # copy all information
         newWriggler.CopyFrom(wriggler)

         nextDest = (move.destColumn, move.destRow)

         #if the head is being moved
         if move.pieceMoved == Move.HEAD:
            newWriggler.MoveWrigglerByHead(nextDest)

         elif move.pieceMoved == Move.TAIL:
            newWriggler.MoveWrigglerByTail(nextDest)

         else:
            raise Exception ("Invalid pieceMoved set in a move!")

         # Update the head and body segment characters
         # XXX - Thought I had a better way to do this...?
         numSegs = len(newWriggler.segments)
         if numSegs > 0:
            newWriggler.head.UpdateSegmentCharacter(newWriggler.segments[0])

            ## Update segments relative to each other
            for segIndex in xrange(0, numSegs-1):
               newWriggler.segments[segIndex].UpdateSegmentCharacter( \
                  newWriggler.segments[segIndex+1])

            newWriggler.segments[-1].UpdateSegmentCharacter(newWriggler.tail)
         else:
            newWriggler.head.UpdateSegmentCharacter(newWriggler.tail)
   except:
      raise

   return newWriggler

# Simple testing below
if __name__ == "__main__":
   # load puzzle one to construct the wriggler
   # it's much easier
   from PuzzleReader import ReadPuzzle
   from WrigglerReader import FindWrigglers
   puzz1 = ReadPuzzle('puzz1.pz')
   wrigglers = FindWrigglers(puzz1)

   # head is at 0, 3
   # tail is at 0, 1
   # try moving the wriggler by the head to the right
   rightMove = Move(0, Move.HEAD, 1, 3)

   # print initial state
   print str(wrigglers[0])
   # attempt the move
   newWriggler = UpdateWriggler(wrigglers[0], rightMove)
   # print post move
   print str(newWriggler)

   # move it again to the right
   rightMove = Move(0, Move.HEAD, 2, 3)

   newWriggler = UpdateWriggler(newWriggler, rightMove)
   print str(newWriggler)

   # Move on to testing the MoveWriggler method
   # First test case, bad input
   #updatedWorldState = MoveWriggler(None, None, None)
   #if updatedWorldState != (None, None):
   #   print "FAILED bad input test!"

   # and a good test
   puzz1.PrintPuzzle()
   print ""
   rightMove = Move(0, Move.HEAD, 1, 3)
   nextState = MoveWriggler(wrigglers[0], rightMove, puzz1)
   nextState[1].PrintPuzzle()

   print ""
   # move the tail up
   tailUp = Move(0, Move.TAIL, 1, 0)
   nextState = MoveWriggler(nextState[0], tailUp, nextState[1])
   nextState[1].PrintPuzzle()

   # Then move the tail right
   print ""
   tailRight = Move(0, Move.TAIL, 2, 0)
   nextState = MoveWriggler(nextState[0], tailRight, nextState[1])
   nextState[1].PrintPuzzle()
