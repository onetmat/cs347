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
   # @param pathCost The "cost" of getting to here from parent
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

if __name__ == "__main__":
   # Test backtracking
   root = SearchNode(None, None, "Root", None)
   last = root
   for x in xrange(1,10):
      next = SearchNode(None, last, "Level : " + str(x), None)
      last = next

   path = last.BackTrack()

   for node in path:
      print node.action
