## @file Agent.py
# @author Mathew Anderson
# @brief Defintion of Agent, common to all types

from SearchNode import SearchNode
from WrigglerMover import MoveWriggler
from SearchNode import State
from PuzzleReader import ReadPuzzle
from WrigglerReader import FindWrigglers
from Move import Move

## This Agent class will form the foundation
# of all Agent classes, but right now is specialized to BFTS
class Agent:

   ## ctor initializes all to empty
   # @param initialSearchNode The starting world state
   def __init__(self, initialSearchNode):
      self.currentSearchNode = initialSearchNode
      self.frontier = []

   ## Determine if the current state is the goal state
   def InGoalState(self):
      # for this puzzle, the goal has been reached when
      # the current state has a wriggler with tail number 0
      # whose head or tail positions coincide with the bottom
      # left hand corner of the maze
      botRightCol = self.currentSearchNode.state.puzzle.numCols - 1
      botRightRow = self.currentSearchNode.state.puzzle.numRows - 1
      botRightTuple = (botRightCol, botRightRow)

      blueWriggler = self.currentSearchNode.state.wrigglers[self.currentSearchNode.state.indexOfBlue]

      return blueWriggler.HeadOrTailAtPos(botRightTuple)

   ## Perform a BFTS for goal node
   def BTFS_Solve(self):
      iterCnt = 0
      # while we're not in the goal state
      # and we haven't interated for "too long"
      while not self.InGoalState() and iterCnt < 1000000000:
         # expand the frontier BTFS style
         self.ExpandFrontier()
         # and move the current node along
         self.currentSearchNode = self.frontier[0]
         self.frontier.remove(self.frontier[0]) # This will kill my time!

   ## If we're in a goal state, construct the solution
   # suitable to be submitted
   def ConstructSolutionString(self):
      solutionString = ''
      if self.InGoalState():
         goalPath = self.currentSearchNode.BackTrack()
         for node in goalPath:
            # root node will not have an action
            if node.action is not None:
               solutionString += str(node.action)

         solutionString += str(self.currentSearchNode.state.puzzle)

      return solutionString

   ## Return the path cost of the current search node
   def GetCurrentSearchNodeCost(self):
      return self.currentSearchNode.pathCost

   ## Perform one BFTS iteration
   # DEBUGGING METHOD
   def BTFSIteration(self):
      # check if the current node is the goal
      if not self.InGoalState():
         # if not, expand the frontier
         self.ExpandFrontier()
         # and set the current node to the top of the frontier
         # XXX Python doesn't have a front method, append + pop
         # will yield last appended value...
         self.currentSearchNode = self.frontier[0]
         self.frontier.remove(self.frontier[0]) # This will kill my time!
      else:
         print "IN GOAL STATE!"
      

   ## Create all possible child states from the current state
   # XXX- BFTS specific
   def ExpandFrontier(self):
      # Query the state for all valid moves for this state
      allMoves = self.currentSearchNode.state.DetermineAllLegalMoves()

      # for each move generate a new search node
      for move in allMoves:
         newSearchNode = self.GenerateSearchNodeFromMove(move)
         # and add it to the frontier
         self.frontier.append(newSearchNode)

   ## Generate a new search node given the current state
   # and a valid move
   # @param move The move to apply
   def GenerateSearchNodeFromMove(self, move):
      # First, determine which wriggler will move
      # and which are not important
      wrigglerDivide = self.SeparateMoveWrigglerFromOthers(move)
      # Next, create a new puzzle and wriggler based on the move
      updatedStateInternals = MoveWriggler(wrigglerDivide[0], \
                                          move, \
                                          self.currentSearchNode.state.puzzle)   

      # put the updated wriggler back with all others
      allWrigglers = [updatedStateInternals[0]]
      if len(wrigglerDivide[1]) > 0:
         allWrigglers.extend(wrigglerDivide[1])
         
      # updateStateInternals = (new wriggler, new world)
      newState = State(updatedStateInternals[1], allWrigglers)
      newSearchNode = SearchNode(newState, \
                                 self.currentSearchNode, \
                                 move, \
                                 self.currentSearchNode.pathCost+1) # XXX - Will need to change this...

      return newSearchNode

   ## Generate a tuple where the first entry is the wriggler
   # affected by a specific move and the second entry is a list
   # of all other wrigglers
   # @param move The move to apply
   def SeparateMoveWrigglerFromOthers(self, move):
      otherWrigglers = []
      moveWriggler = None
      for wriggler in self.currentSearchNode.state.wrigglers:
         if wriggler.tail.idNumber != move.tailNumber:
            otherWrigglers.append(wriggler)
         else:
            moveWriggler = wriggler

      return (moveWriggler, otherWrigglers)

   ## @var currentSearchNode
   # The current state under examination by the agent

   ## @var frontier
   # Collection of states yet to be explored

# BELOW is simple testing code

## Test BFTS iterations
def TestBFTS_Iter():
   puzz1 = ReadPuzzle('puzz1.pz')
   wrig = FindWrigglers(puzz1)

   initialState = State(puzz1, wrig)
   initialSearchNode = SearchNode(initialState, None, None, 0)
   ag = Agent(initialSearchNode)

   print str(ag.currentSearchNode)
   for iter in xrange(1, 10000):
      print "ITER " + str(iter)
      ag.BTFSIteration()

      print str(ag.currentSearchNode)

## Test frontier expansion
def TestFrontierExpand():
   puzz1 = ReadPuzzle('puzz1.pz')
   wrig = FindWrigglers(puzz1)

   initialState = State(puzz1, wrig)
   initialSearchNode = SearchNode(initialState, None, None, 0)
   ag = Agent(initialSearchNode)
   ag.ExpandFrontier()

   for searchNode in ag.frontier:
      print str(searchNode)

## Test basic search node generation
def TestSearchNodeGen():
   puzz1 = ReadPuzzle('puzz1.pz')
   wrig = FindWrigglers(puzz1)

   initialState = State(puzz1, wrig)
   initialSearchNode = SearchNode(initialState, None, None, 0)
   ag = Agent(initialSearchNode)
   mv = Move(0, Move.HEAD, 1, 3)
   newSearchNode = ag.GenerateSearchNodeFromMove(mv)

   path = newSearchNode.BackTrack()

   print str(initialSearchNode.state.puzzle)
   print ""
   for node in path:
      print str(node.action) + " total cost: " + str(node.pathCost)

   print ""
   print str(newSearchNode.state.puzzle)
   print "===="
   print str(newSearchNode)

if __name__ == "__main__":
   from Puzzle import Puzzle
   from Wriggler import Wriggler
   # Test goal state determination
   goalWriggler = Wriggler()
   goalWriggler.head.pos = (1, 2)
   goalWriggler.tail.idNumber = 0
   goalWriggler.tail.pos = (2,2)

   puzz = Puzzle()
   puzz.numCols = 3
   puzz.numRows = 3

   state = State(puzz, [goalWriggler])
   agent = Agent(SearchNode(state, None, None, 0))

   if not agent.InGoalState():
      print "FAILED to detect goal state"

   print "TESTING SEARCH NODE GEN:"
   TestSearchNodeGen()
   print ""
   print "TESTING THE FRONTIER"
   print ""
   TestFrontierExpand()

   print ""
   print "TESTING FULL ITERATIONS"
   TestBFTS_Iter()
   
