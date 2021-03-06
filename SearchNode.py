## @file SearchNode.py
# @author Mathew Anderson
# @brief Implementation of searching node fromm
# Artificial Intelligence: A Modern Approach by Russell and Norvig
from Move import Move
from State import State

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
      self.useHeuristicAndPathCost = False
      self.totalCost = self.GetHeuristicAndPathCost()

   ## Return the cost of the state heuristic plus the path cost required
   # to get to this node
   def GetHeuristicAndPathCost(self):
      return self.state.GetHeuristicCost() + self.pathCost

   ## Query the state for all possible wriggler moves and return them
   def Actions(self):
      return self.state.Actions()

   ## Starting from this SearchNode, construct a path
   # from the root node to this one.
   def BackTrack(self):
      path = [self]
      if self.parent is not None:
         parentList = self.parent.BackTrack()
         parentList.extend(path)
         path = parentList

      return path

   ## Return a hash representation of this SearchNode
   def GetNodeHash(self):
      return self.state.GetPuzzleHash()

   ## For the puzzle project, a SearchNode contains a goal state if
   # the blue wriggler's head or tail is in the lower right hand corner.
   def ContainsGoalState(self):
      return self.state.BlueWrigglerInLowerRightCorner()

   ## Print general info about the puzzle and move, etc
   def __str__(self):
      strRep = ''
      if self.action is not None:
         strRep += str(self.action) + "\n"
      if self.state.puzzle is not None:
         strRep += str(self.state) + "\n"
      strRep += str(self.pathCost)
      return strRep

   ## Determine a strict, weak ordering between this and another
   # SearchNode instance. Used to represent a "cost" function
   def __le__(self, other):
      return self.state.GetHeuristicCost() <= other.state.GetHeuristicCost()

   def __lt__(self, other):
      lessThan = False
      if self.useHeuristicAndPathCost:
         lessThan = \
            self.totalCost < other.totalCost
      else:
         lessThan = \
            self.state.GetHeuristicCost() < other.state.GetHeuristicCost()
      return lessThan

   def __eq__(self, other):
      return self.state.GetDirectPuzzleString() == other.state.GetDirectPuzzleString()

   ## @var state
   # The world state (puzzle) represented by this search node

   ## @var parent
   # The parent search node of this search node (None at root)

   ## @var action
   # The action (Move) that got us to this state from the parent

   ## @var pathCost
   # The cost of getting from the root to this node

   ## @var useHeuristicAndPathCost
   # Set during A* search, uses both heuristic cost and
   # path cost of this node when ordering nodes

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

