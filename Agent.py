## @file Agent.py
# @author Mathew Anderson
# @brief Defintion of Agent, common to all types

from SearchNode import SearchNode
from WrigglerMover import MoveWriggler
from SearchNode import State
from PuzzleReader import ReadPuzzle
from WrigglerReader import FindWrigglers
from Move import Move

# Used to maintain a strict weak ordering on 
import heapq

## This Agent class will form the foundation
# of all Agent classes, but right now is specialized to BFTS
class Agent:

   ## ctor initializes all to empty
   # @param initialSearchNode The starting world state
   def __init__(self, initialSearchNode):
      self.currentSearchNode = None
      self.frontier = [initialSearchNode]

   ## Perform a greedy, best-first search for the goal node
   def GreedyBestFirstGraphSearch(self):
      # frontier contains the initial search node,
      # initialize an explored set as a hash table
      self.explored = dict()

      # remove the initial searchnode
      self.currentSearchNode = self.frontier.pop()

   ## Perform a ID-DTFS search for the goal node
   def IterativeDepthDTFS_Solve(self):
      # Start with a max depth of 1
      currMax = 1

      rootNode = self.frontier[0]

      goalNode = self.RecursiveDFTS_Eval(rootNode, currMax)

      # while this max depth doesn't yield a goal
      while goalNode is None:
         # increment the max
         currMax += 1
         # and try again
         goalNode = self.RecursiveDFTS_Eval(rootNode, currMax)

      # ID-DFTS is complete because all path costs
      # are non-negative and the depth factor is finite
      return goalNode

   ## Given a search node and depth beyond the node to search,
   # perform a depth-limited evaluation of this node
   # @param searchNode The starting search node
   # @param maxDepth The depth from this node we are allowed to go
   def RecursiveDFTS_Eval(self, searchNode, maxDepth):

      # check if this is a goal node,
      # if so, we're done
      if searchNode.ContainsGoalState():
         return searchNode

      # otherwise, determine if this is as deep as we're checking
      if maxDepth == 0:
         # and return no goal found
         return None

      # otherwise, get a list of complete moves
      nextMoves = searchNode.Actions()

      # and for each move
      for nextMove in nextMoves:
         # generate a new node
         nextNode = self.GenerateSearchNodeFromMove(searchNode, nextMove)
         # and recursively evaluate that node, but allowing one less depth
         goalNode = self.RecursiveDFTS_Eval(nextNode, maxDepth - 1)

         #if we find a goal anywhere
         if goalNode is not None:
            # then break out
            return goalNode

   ## Perform a BFTS for goal node
   def BFTS_Solve(self):
      iterCnt = 0
      foundGoal = False
      # while we're not in the goal state
      # and we haven't interated for "too long"
      while not foundGoal and iterCnt < 1000000000:
         # expand the frontier BFTS style
         if len(self.frontier) != 0:
            self.currentSearchNode = self.frontier[0]
            self.frontier.remove(self.frontier[0]) # This will kill my time!
            foundGoal = self.currentSearchNode.ContainsGoalState()

            self.BFTS_ExpandFrontier()
         else:
            break

      return foundGoal

   ## If we're in a goal state, construct the solution
   # suitable to be submitted
   def ConstructSolutionString(self, searchNode):
      solutionString = ''
      if searchNode.ContainsGoalState():
         goalPath = searchNode.BackTrack()
         for node in goalPath:
            # root node will not have an action
            if node.action is not None:
               solutionString += str(node.action)

         solutionString += str(searchNode.state.ConstructSolution())

      return solutionString

   ## Return the path cost of the current search node
   def GetCurrentSearchNodeCost(self):
      return self.currentSearchNode.pathCost

   ## Perform one BFTS iteration
   # DEBUGGING METHOD
   def BFTSIteration(self):
      # check if the current node is the goal
      if not self.self.currentSearchNode.ContainsGoalState():
         # if not, expand the frontier
         self.BFTS_ExpandFrontier()
         # and set the current node to the top of the frontier
         # XXX Python doesn't have a front method, append + pop
         # will yield last appended value...
         self.currentSearchNode = self.frontier[0]
         self.frontier.remove(self.frontier[0]) # This will kill my time!
      else:
         print "IN GOAL STATE!"
      

   ## Create all possible child states from the current state
   def BFTS_ExpandFrontier(self):
      # Query the state for all valid moves for this state
      allMoves = self.currentSearchNode.Actions()

      # for each move generate a new search node
      for move in allMoves:
         newSearchNode = self.GenerateSearchNodeFromMove(self.currentSearchNode, move)
         # and add it to the frontier
         self.frontier.append(newSearchNode)

   ## Generate a new search node given the current state
   # and a valid move
   # @param move The move to apply
   def GenerateSearchNodeFromMove(self, searchNode, move):
      # First, determine which wriggler will move
      # and which are not important
      wrigglerDivide = self.SeparateMoveWrigglerFromOthers(searchNode, move)
      # Next, create a new puzzle and wriggler based on the move
      updatedStateInternals = MoveWriggler(wrigglerDivide[0], \
                                          move, \
                                          searchNode.state.puzzle)   

      # put the updated wriggler back with all others
      allWrigglers = [updatedStateInternals[0]]
      if len(wrigglerDivide[1]) > 0:
         allWrigglers.extend(wrigglerDivide[1])
         
      # updateStateInternals = (new wriggler, new world)
      newState = State(updatedStateInternals[1], allWrigglers)
      newSearchNode = SearchNode(newState, \
                                 searchNode, \
                                 move, \
                                 searchNode.pathCost+1) # XXX - Will need to change this...

      return newSearchNode

   ## Generate a tuple where the first entry is the wriggler
   # affected by a specific move and the second entry is a list
   # of all other wrigglers
   # @param move The move to apply
   def SeparateMoveWrigglerFromOthers(self, searchNode, move):
      otherWrigglers = []
      moveWriggler = None
      for wriggler in searchNode.state.wrigglers:
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
      ag.BFTSIteration()

      print str(ag.currentSearchNode)

## Test frontier expansion
def TestFrontierExpand():
   puzz1 = ReadPuzzle('puzz1.pz')
   wrig = FindWrigglers(puzz1)

   initialState = State(puzz1, wrig)
   initialSearchNode = SearchNode(initialState, None, None, 0)
   ag = Agent(initialSearchNode)
   ag.BFTS_ExpandFrontier()

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
   newSearchNode = ag.GenerateSearchNodeFromMove(initialSearchNode, mv)

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

   if not agent.currentSearchNode.ContainsGoalState():
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
   
