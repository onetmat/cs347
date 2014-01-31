## @file Wriggler.py
# @author Mathew Anderson
# @brief Contains complete wriggler representation

## The BodySegment class represents a non-head, non-tail segment
# of a Wriggler. Head and Tail have implicit representations
class BodySegment:

   ## Symbolic constants for body segments
   # these represent the direction of the next segment
   SEGMENT_CHARS = ['^', '>', 'v', '<']

   ## Ctor initializes all member vars to 0
   def __init__(self):
      self.dirOfNext = 0
      self.pos = (0, 0)

   ## @var dirOfNext
   # Symbolic representation of the direction of the next segment

   ## @var pos
   # Tuple representing the current position of a body segment

## The Wriggler class stores the locations and
# appropriate attributes for each segment of a wriggler
# including the head and tail
class Wriggler:

   ## Symbolic constants for head segments
   # these indicate the direction of the next body segment
   HEAD_CHARS = ['U', 'R', 'D', 'L']

   ## Ctor sets all member variables to 0
   def __init__(self):
      self.head.dirOfNext = 0
      self.head.pos = (0, 0)

      self.tail.idNumber = 0
      self.tail.pos = (0, 0)

      self.segments = []

   ## @var head
   # Wriggler's head is (dir of next segment, (col, row) position in puzzle of head

   ## @var tail
   # Tail is (ID number, (col, row) position)

   ## @var segments
   # List of segments, where a segment is a (dir of next segment, (col, row) position)
