## @file Wriggler.py
# @author Mathew Anderson
# @brief Contains complete wriggler representation

## Symbolic constants for body segments
# these represent the direction of the next segment
SEGMENT_CHARS = ['^', '>', 'v', '<']

## Symbolic constants for head segments
# these indicate the direction of the next body segment
HEAD_CHARS = ['U', 'R', 'D', 'L']

## The BodySegment class represents a non-head, non-tail segment
# of a Wriggler. Head and Tail have implicit representations
class BodySegment:


   ## Ctor initializes all member vars to 0
   def __init__(self):
      self.dirOfNext = 0
      self.pos = (0, 0)

   ## @var dirOfNext
   # Symbolic representation of the direction of the next segment

   ## @var pos
   # Tuple representing the current position of a body segment

## The HEAD has a special representation
# and a position, but otherwise nothing special
class Head:

   ## Ctor initialize all values to 0
   def __init__(self):
      self.dirOfNext = 0
      self.pos = (0, 0)

   ## @var dirOfNext
   # Character representation of the direction of the next segment

   ## @var pos
   # Position in the puzzle of the head

## The TAIL has a number identifying the wriggler
# and a position, but otherwise nothing special
class Tail:
   ## Ctor initializes everything to 0
   def __init__(self):
      self.idNumber = 0
      self.pos = (0, 0)

## The Wriggler class stores the locations and
# appropriate attributes for each segment of a wriggler
# including the head and tail
class Wriggler:


   ## Ctor sets all member variables to 0
   def __init__(self):
      self.head = Head()

      self.tail = Tail()

      self.segments = []

   ## ToString method that prints something useful
   # beyond the object hash.
   def __str__(self):
      strRep = "Head char, location: " + self.head.dirOfNext + ", " + str(self.head.pos)
      strRep += "\nTail number, location: " + str(self.tail.idNumber) + ", " + str(self.tail.pos)

      segNum = 1
      for segment in self.segments:
         strRep += "\nSegment number " + str(segNum) + " char, location: " + segment.dirOfNext \
            + ", " + str(segment.pos)

      strRep += "\n"
      return strRep

   ## @var head
   # Wriggler's head is (dir of next segment, (col, row) position in puzzle of head

   ## @var tail
   # Tail is (ID number, (col, row) position)

   ## @var segments
   # List of segments, where a segment is a (dir of next segment, (col, row) position)
