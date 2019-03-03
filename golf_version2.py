# importing necessary modules
import copy
import queue
import time
import random
import sys

class golf:
    """
    class State creates state objects for the given puzzle
    """
    def __init__(self):
        """
        constructor initiales necessary variables used throughout the program
        """
        self.width = 0
        self.height = 0
        self.potentialLoc = []
        self.obstaclesLoc = []
        self.ballPos = []
        self.goalPos = []
        self.actionRecord = []
        self.h_cost = 0
        
    def course(self):
        """
        this function reads the puzzle file, parses it to get the puzzle grid, size of the grid, and the number of worms
        """
        grid = []
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            for line in f:
                myList = []
                for word in line.split():
                    myList.append(word)  
                grid.append(myList)

        # assigning the width and height of the grid and number of worms in the grid to the respective variables
        self.width = int(grid[0][0])
        self.height = int(grid[0][1])

        del grid[0]

        # assigning all the empty locations from the grid to the list of empty locations
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "e":
                    self.potentialLoc.append([i, j])

        # assigning all the wall locations from the grid to the list of wall locations
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "x":
                    self.obstaclesLoc.append([i, j])

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == "b":
                    self.ballPos = [row, col]
        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == "O":
                    self.goalPos = [row, col]

    def __eq__(self, otherState):
        return self.ballPos == otherState.ballPos
                    
    def heuristic_fBonus(self):
        r, c = grid.ballPos
        listCost = []

        for rowAdd, colAdd in [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            cost = 0
            row, col = r, c
            for direction in range(2):
                row, col = r+rowAdd, c+colAdd
                while col < self.height and row < self.width:
                    row, col = row+rowAdd, col+colAdd
                    cost += 1
                    if [row, col] == self.goalPos:
                        cost += 2
                rowAdd, colAdd = colAdd, rowAdd

            if cost > 0:
                listCost.append(cost)

        self.h_cost = min(listCost)
        #print("h_cost", self.h_cost)

        return self.h_cost


def action(grid):
    """
    this function generates next possible moves for the worm and takes in the current state
    """
    nextMoves = []
    r, c = grid.ballPos
    #print("r,c", r,c)

    for row, col in [(r, c+1), (r, c-1), (r+1, c), (r-1, c), (r+1, c+1), (r-1, c-1), (r+1, c-1), (r-1, c+1)]:
        #(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)
        if [row, col] in grid.potentialLoc or [row, col] == grid.goalPos:
            nextMoves.append([row, col])
    
    #print("next m", nextMoves)
    return nextMoves

def transitionModel(grid, action):
    """
    this is a transition model that takes the current state and applies the next possible moves to generate new states
    """
    newGrid = copy.deepcopy(grid)

    newGrid.ballPos = action
    newGrid.potentialLoc.append(newGrid.ballPos)
    newGrid.potentialLoc.remove(action)

    return newGrid


def GBeFGS(st):
    frontier = queue.PriorityQueue()
    explored = []
    counter = 0
    
    explored.append(st)
    
    while True:
        #print("while")
        if st.ballPos == st.goalPos:
            break
        
        explored.append(st)
        act = action(st)
        st.actionRecord.append(st.ballPos)
        
        for a in act:
            #print("action", a)
            currentState = transitionModel(st, a)
            
            if currentState not in explored:
                frontier.put((currentState.h_cost, counter, currentState))
                currentState.actionRecord.append(a)
                explored.append(currentState)
            counter += 1
        
        if frontier.empty():
            break
        
        priorNum, newCounter, st = frontier.get()

        if st.ballPos == st.goalPos:
            break
            
    return st


initgrid = golf()
initgrid.course()
goalGrid = GBeFGS(initgrid)

def grid(st):
    """
    this function creates a grid for any current state
    """
    
    # using current worm segments to visualize where the worm is in the grid
    # wormsList = st.listWorms

    st.grid = [[None for i in range(st.width)] for j in range(st.height)]

    # if the next part of the worm is towards left, head is indicated with "L", if right then "R",
    # if up then "U", and if down then "D"
    x, y = st.ballPos
    st.grid[x][y] = "b"
    
    a, b = st.goalPos
    st.grid[a][b] = "O"

    for e in st.obstaclesLoc:
        x, y = e
        st.grid[x][y] = "x"

    # plotting the updated empty locations
    for e in st.potentialLoc:
        x, y = e
        st.grid[x][y] = "e"

    return st.grid


def solutionFile(st):
    """
    this function takes the path from initial state to the goal state and outputs 
    the information required for the assignment
    """
    # recording number of moves from initial state to the goal state
    #numMoves = len(st.actionRecord)
    #numMoves = st.depth
    
    finalGrid = grid(st)
    for x in finalGrid:
        print(*x, sep="")

solutionFile(initgrid)
