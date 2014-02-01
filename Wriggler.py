## @file Wriggler.py
# @author Mathew Anderson
# @brief Contains complete wriggler representation

## Symbolic indices into the character representation
# lists (below)
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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
      self.myReps = SEGMENT_CHARS

   ## Clone a BodySegment instance
   # @param other Source of clone
   def CopyFrom(self, other):
      self.pos = tuple(other.pos)
      self.dirOfNext = other.dirOfNext
      # ignore the myreps


   ## Set new position of segment
   # @param newPos Position of segment
   def MoveTo(self, newPos):
      self.pos = newPos

   ## Updates the character that represents this character
   # @param other The segment relative to this one
   def UpdateSegmentCharacter(self, other):
      segmentDelta = self.DetermineSegmentDelta(other)
      self.DetermineCharacterFromDelta(segmentDelta)

   ## Determine the delta in position from another segment
   # @param other The other BodySegment
   # @return A tuple containing the delta
   def DetermineSegmentDelta(self, other):
      # Determined experimentally that this is proper
      colDelta = self.pos[0] - other.pos[0]
      rowDelta = self.pos[1] - other.pos[1]
      return (colDelta, rowDelta)

   ## Given a position delta, determine which character
   # representation is appropriate
   # @param delta A (col, row) type that represents a recent move
   # @note This class changes the dirOfNext variable of this class
   def DetermineCharacterFromDelta(self, delta):
      try:
         # validate input, only one non-zero entry in tuple
         colIsChanging = int(delta[0]) != 0
         rowIsChanging = int(delta[1]) != 0

         # input normalized to boolean, XOR is now boolA != boolB
         if colIsChanging != rowIsChanging:

            if colIsChanging:
               # moving left or right
               movingLeft = int(delta[0]) == -1

               if movingLeft:
                  self.dirOfNext = self.myReps[RIGHT]

               else:
                  # next will be to the left
                  self.dirOfNext = self.myReps[LEFT]
            else:
               # moving up or down
               movingUp = int(delta[1]) == -1

               if movingUp:
                  # next segment will be down
                  self.dirOfNext = self.myReps[DOWN]

               else:
                  # next segment will be up
                  self.dirOfNext = self.myReps[UP]
         else:
            raise Exception("Invalid delta: " + str(delta))
      except:
         raise

   ## @var dirOfNext
   # Symbolic representation of the direction of the next segment

   ## @var pos
   # Tuple representing the current position of a body segment

   ## @var myReps
   # Character representation of all possible "next" segments

## The HEAD has a special representation
# and a position, but otherwise nothing special
class Head(BodySegment):

   ## Ctor initialize all values to 0
   # Head has custom char reps
   def __init__(self):
      BodySegment.__init__(self)
      self.myReps = HEAD_CHARS


## The TAIL has a number identifying the wriggler
# and a position, but otherwise nothing special
# tail never changes it's character
class Tail(BodySegment):
   ## Ctor initializes everything to 0
   def __init__(self):
      BodySegment.__init__(self)
      self.idNumber = 0

   ## Clone a Tail object
   # @param other The source of the clone
   def CopyFrom(self, other):
      BodySegment.CopyFrom(self, other)
      self.idNumber = other.idNumber
      

   ## Tail's character never changes. It's classy like that.
   def DetermineCharacterFromDelta(self, delta):
      return self.idNumber


## The Wriggler class stores the locations and
# appropriate attributes for each segment of a wriggler
# including the head and tail
class Wriggler:


   ## Ctor sets all member variables to 0
   def __init__(self):
      self.head = Head()

      self.tail = Tail()

      self.segments = []

   ## Copy an existing Wriggler
   # @param other A other wriggler
   def CopyFrom(self, other):
      self.head.CopyFrom(other.head)
      self.tail.CopyFrom(other.tail)
      for otherSegment in other.segments:
         newSegment = BodySegment()
         newSegment.CopyFrom(otherSegment)
         self.segments.append(newSegment)
      

   ## ToString method that prints something useful
   # beyond the object hash.
   def __str__(self):
      strRep = "Head char, location: " + self.head.dirOfNext + ", " + str(self.head.pos)
      strRep += "\nTail number, location: " + str(self.tail.idNumber) + ", " + str(self.tail.pos)

      segNum = 1
      for segment in self.segments:
         strRep += "\nSegment number " + str(segNum) + " char, location: " + segment.dirOfNext \
            + ", " + str(segment.pos)
         segNum += 1

      strRep += "\n"
      return strRep

   ## @var head
   # Wriggler's head is (dir of next segment, (col, row) position in puzzle of head

   ## @var tail
   # Tail is (ID number, (col, row) position)

   ## @var segments
   # List of segments, where a segment is a (dir of next segment, (col, row) position)

# basic testing
if __name__ == "__main__":
   bs = BodySegment()
   bs.dirOfNext = '^'
   bs.pos = (2, 3)

   # Try moving down, verify char rep is lower case v
   print "bs was: " + bs.dirOfNext
   bs.DetermineCharacterFromDelta((0, -1))
   if bs.dirOfNext != 'v':
      print "FAILED"
   print "bs is: " + bs.dirOfNext

   head = Head()
   head.dirOfNext = 'L'
   head.pos = (1,1)

   print "head was: " + head.dirOfNext
   # trying moving down
   head.DetermineCharacterFromDelta((0, 1))
   if head.dirOfNext != 'U':
      print "FAILED"
   print "head is: " + head.dirOfNext

# XXX - Wriggler needs tighter definition.
# XXX - For proj two, see why moving was such a pain
# XXX - Modify these classes to have getters/setters - too hard
# to test with live data (at Puzzle and Agent level)
