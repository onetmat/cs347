## @file WrigglerReader.py
# @author Mathew Anderson
# @brief Contains methods to extract wrigglers from a puzzle

from Puzzle import Puzzle
from Wriggler import BodySegment, Wriggler

## Given a puzzle or world state, extract all Wrigglers
# returning them in a list
# @param puzzle The puzzle instance from which wrigglers are desired
def FindWrigglers(puzzle):
   # initialize return value
   wrigglers = []
   # initialize loop variables
   # zero based due to indexing in Puzzle
   currCol = 0
   currRow = 0
   # If Puzzle is valid
   try:
      # Foreach column
      while currCol < puzzle.numCols:
         # foreach row
         while currRow < puzzle.numRows:
            # if this puzzle tile indicates a Wriggler head
            if puzzle.GetTile(currCol, currRow) in Wriggler.HEAD_CHARS:
               # try to extract it
               nextWriggler = ExtractWriggler((currCol, currRow), puzzle)
               # and append it to the list if successful
               if nextWriggler is not None:
                  wrigglers.append(nextWriggler)
   except AttributeError as e:
      # invalid Puzzle passed, return empty string
      print "Unable to find any Wrigglers in arg passed: " + e.message
      wrigglers = []
   return wrigglers

## Given a (col, row) tuple representation the location of a wriggler
# head, follow and extract the segments and construct a wriggler
# @param headLocation A tuple (col, row) into the puzzle where the head character
# was found
# @param puzzle The puzzle instance
def ExtractWriggler(headLocation, puzzle):
   nextWriggler = None
   return nextWriggler

## Given a head or body segment and a current (col, row) position
# produce the location of the next segment
def GetDirectionOfNextSegment(segmentChar, currentPos):
   # start by storing the old position in pieces
   nextCol = currentPos[0]
   nextRow = currentPos[1]
   # then alter the variables according to what the current
   # character is
   if segmentChar == 'U' or segmentChar == '^':
      # move up one row
      nextRow -= 1
   elif segmentChar == 'R' or segmentChar == '>':
      # to the right one col
      nextCol += 1
   elif segmentChar == 'D' or segmentChar == 'v':
      # down a row
      nextRow += 1
   elif segmentChar == 'L' or segmentChar == '<':
      # left one col
      nextCol -= 1
   else:
      raise Exception("Invalid character presented to GetDirectionOfNextSegment!!")

   nextPos = (nextCol, nextRow)
   return nextPos

if __name__ == "__main__":
   import PuzzleReader
   tstPuzz = PuzzleReader.ReadPuzzle('puzz1.pz')

   # first test GetDirectionOfNextSegment
   nextDir = GetDirectionOfNextSegment('U', (1, 1))
   if nextDir != (1, 0):
      print "FAILED to move up a row!"
   else:
      print "(1, 1) + U = " + str(nextDir)

   nextDir = GetDirectionOfNextSegment('>', (1, 1))
   if nextDir != (2, 1):
      print "FAILED to move right a column!"
   else:
      print "(1, 1) + > = " + str(nextDir)

   nextDir = GetDirectionOfNextSegment('v', (1, 1))
   if nextDir != (1, 2):
      print "FAILED to move down a row!"
   else:
      print "(1, 1) + v = " + str(nextDir)

   nextDir = GetDirectionOfNextSegment('L', (1, 1))
   if nextDir != (0, 1):
      print "FAILED to move left a column!"
   else:
      print "(1, 1) + L = " + str(nextDir)

