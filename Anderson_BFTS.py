## @file Anderson_BTFS.py
# @author Mathew Anderson
# @brief Implementation of main method
# for CS347SP14 Puzzle Project part I - BFTS

from PuzzleReader import ReadPuzzle

from WrigglerReader import FindWrigglers

# prompt for file name
puzzleFile = raw_input('Enter filename of puzzle: ')

# attempt to construct the initial state
initialState = ReadPuzzle(puzzleFile)

# attempt to extract all wriggler info
wrigglers = FindWrigglers(initialState)

# Initial debug - just print the puzzle and the wrigglers
initialState.PrintPuzzle()

for wrig in wrigglers:
   print wrig
