## @file Agent.py
# @author Mathew Anderson
# @brief Defintion of Agent, common to all types

from SearchNode import SearchNode

class Agent:

   ## ctor initializes all to empty
   def __init__(self):
      self.currentSearchNode = None
      self.frontier = []

   ## Determine if the current state is the goal state
   def InGoalState(self):
      goalState = False
      # for this puzzle, the goal has been reached when
      # the current state has a wriggler with tail number 0
      # whose head or tail positions coincide with the bottom
      # left hand corner of the maze
      botRightCol = self.currentSearchNode.state.puzzle.numCols - 1
      botRightRow = self.currentSearchNode.state.puzzle.numRows - 1
      botRightTuple = (botRightCol, botRightRow)

      blueWriggler = self.currentSearchNode.state.wrigglers[self.currentSearchNode.state.indexOfBlue]

      if botRightTuple == blueWriggler.head.pos or botRightTuple == blueWriggler.tail.pos:
         goalState = True

      return goalState

   ## @var currentSearchNode
   # The current state under examination by the agent

   ## @var frontier
   # Collection of states yet to be explored


if __name__ == "__main__":
   from SearchNode import State
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
   agent = Agent()
   agent.currentSearchNode = SearchNode(state, None, None, 0)

   if not agent.InGoalState():
      print "FAILED to detect goal state"
   
