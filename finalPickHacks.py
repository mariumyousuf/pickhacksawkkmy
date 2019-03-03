# importing necessary modules
import copy
import queue
import time
import random
import sys
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

class golf:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.potentialLoc = []
        self.obstaclesLoc = []
        self.ballPos = []
        self.goalPos = []
        self.actionRecord = []
        self.h_cost = 0
        
    def course(self):
        grid = []
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            for line in f:
                myList = []
                for word in line.split():
                    myList.append(word)  
                grid.append(myList)

        self.width = int(grid[0][0])
        self.height = int(grid[0][1])

        del grid[0]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "e":
                    self.potentialLoc.append([i, j])

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
        print("h_cost", self.h_cost)

        return self.h_cost

def action(grid):
    nextMoves = []
    r, c = grid.ballPos

    for row, col in [(r, c+1), (r, c-1), (r+1, c), (r-1, c), (r+1, c+1), (r-1, c-1), (r+1, c-1), (r-1, c+1)]:
        if [row, col] in grid.potentialLoc or [row, col] == grid.goalPos:
            nextMoves.append([row, col])
    
    return nextMoves

def transitionModel(grid, action):
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
        if st.ballPos == st.goalPos:
            break
        
        explored.append(st)
        act = action(st)
        st.actionRecord.append(st.ballPos)
        
        for a in act:
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

def grid(st):
    st.grid = [[None for i in range(st.width)] for j in range(st.height)]

    x, y = st.ballPos
    st.grid[x][y] = 0
    
    a, b = st.goalPos
    st.grid[a][b] = 1

    for e in st.obstaclesLoc:
        x, y = e
        st.grid[x][y] = 2

    # plotting the updated empty locations
    for e in st.potentialLoc:
        x, y = e
        st.grid[x][y] = 3
        
    for e in st.actionRecord:
        x, y = e
        st.grid[x][y] = 4

    return st.grid

initgrid = golf()
initgrid.course()
goalGrid = GBeFGS(initgrid)

a = np.asarray(grid(initgrid))
sns.heatmap(a, cmap=ListedColormap(['yellow', 'black', 'green', 'pink']), cbar=False, xticklabels=False, yticklabels=False)
fig = plt.gcf()
fig.set_size_inches(5,5)
plt.show()

b = np.asarray(grid(goalGrid))
sns.heatmap(b, cmap=ListedColormap(['black', 'red', 'green', 'white']), cbar=False, xticklabels=False, yticklabels=False)
fig = plt.gcf()
fig.set_size_inches(5,5)
plt.show()

