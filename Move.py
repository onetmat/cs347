## @file Move.py
# @author Mathew Anderson
# @brief Definition of Move class

## The Move class completely defines a valid move that can be executed.
# Moves are applied to a world state to transition from one state to another.
# In addition, the Move class is capable of printing output in accordance with
# the project specification.
class Move:

   ## Symbolic constant indicating the head piece of a wriggler is being moved
   HEAD = 0
   ## Symbolic constant indicating the tail piece of a wriggler is being moved
   TAIL = 1

   ## Ctor that allows initial conditions to be set
   def __init__(self, tailNumber, pieceMoved, destColumn, destRow):
      self.tailNumber = tailNumber
      self.pieceMoved = pieceMoved
      self.destColumn = destColumn
      self.destRow = destRow

   ## Print the move in the format specified in the project
   # <Wriggler ID> <HEAD or TAIL> <Destination Column> <Destination Row>
   # @param tgtFile An (optional) open text file to which the output should be written
   # if set to None (default) will output to stdout
   def printMove(self, tgtFile=None):
      # Setup a "plain text" string (using whatever character encoding
      # is in play when executed
      outputString = str(self.tailNumber) + ' ' \
                     + str(self.pieceMoved) + ' ' \
                     + str(self.destColumn) + ' ' \
                     + str(self.destRow) + '\n'

      # try to write to the file
      try:
         tgtFile.write(outputString)
      except:
         # print to stdout
         print outputString

   ## Same as PrintMove but works with str operator
   def __str__(self):
      outputString = str(self.tailNumber) + ' ' \
                     + str(self.pieceMoved) + ' ' \
                     + str(self.destColumn) + ' ' \
                     + str(self.destRow) + '\n'

      return outputString


   ## @var tailNumber
   # Uniquely identifies wriggler being moved

   ## @var pieceMoved
   # Can be either HEAD or TAIL, indicating either the head or tail is
   # being moved respectively

   ## @var destColumn
   # Indicates the destination column of the piece being moved

   ## @var destRow
   # indicates the destination row of the piece being moved`

# Informal unit testing harness
if __name__ == "__main__":
   # first try writing a None move to stdout
   m = Move(0, 0, 0, 0)
   m.printMove()

   # Then try writing a meaningful move
   m = Move(0, Move.TAIL, 2, 2)
   m.printMove()

   # And then try writing it to a file
   outFile = open('movetest.out', 'w')
   m.printMove(outFile)
   outFile.close()
