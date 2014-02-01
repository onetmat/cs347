## @file SearchNode.py
# @author Mathew Anderson
# @brief Implementation of searching node fromm
# Artificial Intelligence: A Modern Approach by Russell and Norvig
from Move import Move

## The SearchNode class tracks the state of the world
# and all other variables that are useful to an agent.
# This comes from p 78 of the aformentioned book
# modified to suit this programming project
class SearchNode:

   ## Ctor sets up instance vars
   # @param state Initial state of the world
   # @param parent The parent node of this search node
   # @param action The action that got us from parent to here
   # @param pathCost The "cost" of getting to here from root
   def __init__(self, state, parent, action, pathCost):
      self.state = state
      self.parent = parent
      self.action = action
      self.pathCost = pathCost

   ## Starting from this SearchNode, construct a path
   # from the root node to this one.
   def BackTrack(self):
      path = [self]
      if self.parent is not None:
         parentList = self.parent.BackTrack()
         parentList.extend(path)
         path = parentList

      return path

   ## Print general info about the puzzle and move, etc
   def __str__(self):
      strRep = ''
      if self.action is not None:
         strRep += str(self.action) + "\n"
      if self.state.puzzle is not None:
         strRep += str(self.state.puzzle) + "\n"
      strRep += str(self.pathCost)
      return strRep

   ## @var state
   # The world state (puzzle) represented by this search node

   ## @var parent
   # The parent search node of this search node (None at root)

   ## @var action
   # The action (Move) that got us to this state from the parent

   ## @var pathCost
   # The cost of getting from the root to this node

## The state class contains relevant information to our puzzle assignment
class State:
   ## Ctor tags instances, determines who is blue
   def __init__(self, puzzle, wrigglers):

      self.puzzle = puzzle
      self.wrigglers = wrigglers
      self.indexOfBlue = 0

      for index, wriggler in list(enumerate(self.wrigglers)):
         if wriggler.tail.idNumber == 0:
            self.indexOfBlue = index

  
   ## Determines all legal moves from this state 
   # @return A list of all legal moves (Move objects)
   def DetermineAllLegalMoves(self):
      legalMoves = []

      for wriggler in self.wrigglers:
         wrigglerMoves = self.GetLegalMovesFromWriggler(wriggler)

         if len(wrigglerMoves) > 0:
            legalMoves.extend(wrigglerMoves)
      
      return legalMoves

   ## Cull illegal (out of bounds/occupied) moves from a wriggler
   # @param wriggler to check
   # @return List of all legal moves from this state that a particular wriggler
   # can make
   def GetLegalMovesFromWriggler(self, wriggler):
      allMoves = self.GetAllMovesFromWriggler(wriggler)
      legalMoves = []

      # remove out of bounds or occupied squares
      for move in allMoves:

         moveInBounds = self.puzzle.PositionInBounds(move.destColumn, move.destRow)
         if moveInBounds:
            tileOpen = self.puzzle.IsOpen(move.destColumn, move.destRow)

            if tileOpen:
               legalMoves.append(move)

      return legalMoves

   ## Determine all possible moves from a wriggler head/tail
   # @param wriggler Data form which moves will be created
   # @return A list of Move objects
   def GetAllMovesFromWriggler(self, wriggler):
      # All possible moves of moving up, down, left, right one
      # (col, row) for each entry
      allMoves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
      movesFromWriggler = []
      # generate moves from the head and tail
      for move in allMoves:
         headMoveDest = (wriggler.head.pos[0] + move[0], wriggler.head.pos[1] + move[1])
         headMove = Move(wriggler.tail.idNumber, Move.HEAD, headMoveDest[0], headMoveDest[1])

         tailMoveDest = (wriggler.tail.pos[0] + move[0], wriggler.tail.pos[1] + move[1])
         tailMove = Move(wriggler.tail.idNumber, Move.TAIL, tailMoveDest[0], tailMoveDest[1])

         movesFromWriggler.extend([headMove, tailMove])

      return movesFromWriggler

   ## @var puzzle
   # The current world state

   ## @var wrigglers
   # Collection of wrigglers in play

   ## @var indexOfBlue
   # Index of the wriggler whose goal it is to have head or tail
   # in lower right hand corner
   

if __name__ == "__main__":
   # Test backtracking
   root = SearchNode(None, None, "Root", 0)
   last = root
   for x in xrange(1,10):
      next = SearchNode(None, last, "Level : " + str(x), last.pathCost + 1)
      last = next

   path = last.BackTrack()

   for node in path:
      print node.action + " total cost: " + str(node.pathCost)

   # test legal move determination
   from PuzzleReader import ReadPuzzle
   from WrigglerReader import FindWrigglers

   puzz = ReadPuzzle('puzz1.pz')
   wrigglers = FindWrigglers(puzz)
   state = State(puzz, wrigglers)

   allLegalMoves = state.DetermineAllLegalMoves()

   for move in allLegalMoves:
      print str(move)
