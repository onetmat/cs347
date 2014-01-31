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
# @returns A new world state reflecting the move or None on error
def MoveWriggler(wriggler, move, puzzle):
   newPuzzle = None
   try:
      # First, update the wriggler itself to get the correct characters
      # the update method returns a new wriggler, so we can clear
      # out the characters from the puzzle
      # Then, update the puzzle with the new wriggler information
      pass

   except Exception as e:
      print "Failed to MoveWriggler: " + e.message
      newPuzzle = None

   return newPuzzle

## Given a wriggler and a move, update the positions
# and all character representations of the segments
# @param wriggler The wriggler to move
# @param Information about the move
# @return A new Wriggler instance that incorporates the move
# or None on error
def UpdateWrigger(wriggler, move):

   newWriggler = None
   # Given valid input
   try:
      if move.tailNumber == wriggler.tail.idNumber:
         #if the head is being moved
         if move.pieceMoved == Move.HEAD:
            # determine if either row or column is changing
            rowDelta = wriggler.

         elif move.pieceMoved == Move.TAIL:

   except Exception as e:
      raise Exception ("Unable to UpdateWriggler: " + e.message)
   return newWriggler

# Simple testing below
if __name__ == "__main__":


   # Move on to testing the MoveWriggler method
   # First test case, bad input
   updatedWorldState = MoveWriggler(None, None, None)
   if updatedWorldState is not None:
      print "FAILED bad input test!"
   pass
