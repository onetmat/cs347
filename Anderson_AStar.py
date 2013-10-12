## @file Anderson_AStar.py
# @author Mathew Anderson
# @brief Implementation of main method
# for CS347SP14 Puzzle Project part IV - A* Search

from PuzzleReader import ReadPuzzle
from WrigglerReader import FindWrigglers
from Agent import Agent
from SearchNode import State, SearchNode
import time

# prompt for file name
puzzleFile = raw_input('Enter filename of puzzle: ')

# attempt to construct the initial state
initialPuzzle = ReadPuzzle(puzzleFile)

if initialPuzzle is not None:
   # attempt to extract all wriggler info
   wrigglers = FindWrigglers(initialPuzzle)

   if len(wrigglers) > 0:
      initialState = State(initialPuzzle, wrigglers)
      initialSearchNode = SearchNode(initialState, None, None, 0)

      smith = Agent(initialSearchNode)
      startTime = time.clock()
      foundGoal = smith.AStarSearch()
      endTime = time.clock()

      if foundGoal is not None:
         solution = smith.ConstructSolutionString(foundGoal)
         solnFile = open(puzzleFile + '.sln', 'w')
         solnFile.write(solution + '\n')
         solnFile.write(str(endTime - startTime) + '\n')
         solnFile.write(str(foundGoal.pathCost) + '\n')
