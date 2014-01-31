## @file WrigglerReader.py
# @author Mathew Anderson
# @brief Contains methods to extract wrigglers from a puzzle

from Puzzle import Puzzle
from Wriggler import BodySegment, Wriggler, HEAD_CHARS, SEGMENT_CHARS

## Given a puzzle or world state, extract all Wrigglers
# returning them in a list
# @param puzzle The puzzle instance from which wrigglers are desired
def FindWrigglers(puzzle):
   # initialize return value
   wrigglers = []
   # initialize loop variables
   # zero based due to indexing in Puzzle
   currCol = 0
   # If Puzzle is valid
   try:
      # Foreach column
      while currCol < puzzle.numCols:
         # foreach row
         currRow = 0
         while currRow < puzzle.numRows:
            # if this puzzle tile indicates a Wriggler head
            if puzzle.GetTile(currCol, currRow) in HEAD_CHARS:
               # try to extract it
               nextWriggler = ExtractWriggler((currCol, currRow), puzzle)
               # and append it to the list if successful
               if nextWriggler is not None:
                  wrigglers.append(nextWriggler)
            currRow += 1
         currCol += 1
   except AttributeError as e:
      # invalid Puzzle passed, return empty string
      print "Unable to find any Wrigglers in arg passed: " + e.message
      wrigglers = []
   except Exception as e:
      print "Something wrong while extraction specific Wriggler: " + e.message
      wrigglers = []
   return wrigglers

## Given a (col, row) tuple representation the location of a wriggler
# head, follow and extract the segments and construct a wriggler
# @param headLocation A tuple (col, row) into the puzzle where the head character
# was found
# @param puzzle The puzzle instance
def ExtractWriggler(headLocation, puzzle):
   # It all starts with the head, so extract that character
   headChar = puzzle.GetTile(headLocation[0], headLocation[1])
   # Create the new wriggler and store the head info
   nextWriggler = Wriggler()
   nextWriggler.head.dirOfNext = headChar
   nextWriggler.head.pos = headLocation

   # while we haven't found the tail
   foundTail = False
   currentChar = headChar
   currentPos = headLocation

   while not foundTail:
      # Get the next position to examine
      nextPos = GetDirectionOfNextSegment(currentChar, currentPos)

      # Get the next character to examine
      nextChar = puzzle.GetTile(nextPos[0], nextPos[1])

      # if it's a body segment
      if nextChar in SEGMENT_CHARS:
         # Create a new body segment
         nextBodySeg = BodySegment()
         nextBodySeg.dirOfNext = nextChar
         nextBodySeg.pos = nextPos
         nextWriggler.segments.append(nextBodySeg)

         # store the current pos and char
         currentChar = nextChar
         currentPos = nextPos
         # and move on
      else:
         # if it's a number, it's the tail
         try:
            nextWriggler.tail.idNumber = int(nextChar)
            nextWriggler.tail.pos = nextPos
            foundTail = True
         except:
            # not the tail and not the body segment => problem
            raise Exception("Encountered a non-body, non-tail char: " + nextChar)

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

   # Next try extract a wriggler from a known location
   import PuzzleReader
   tstPuzz = PuzzleReader.ReadPuzzle('puzz1.pz')

   theWriggler = ExtractWriggler((0, 3), tstPuzz)

   print theWriggler

   # Next, try to extract a wriggler from a puzzle
   # with > 1
   tstPuzz2 = PuzzleReader.ReadPuzzle('puzz2.pz')
   wrigglers = FindWrigglers(tstPuzz2)

   for wrig in wrigglers:
      print wrig
