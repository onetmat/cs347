## @file SearchNode.py
# @author Mathew Anderson
# @brief Implementation of searching node fromm
# Artificial Intelligence: A Modern Approach by Russell and Norvig

## THe SearchNode class tracks the state of the world
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

   
   def DetermineAllLegalMoves(self):
      pass

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
