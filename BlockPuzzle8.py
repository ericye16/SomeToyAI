#!/usr/bin/env python
#let's try and implement that block puzzle.

import Queue

initState = [[7, 2, 4],
            [5, 0, 6],
            [8, 3, 1]]

actions = ['L', 'R', 'U', 'D']
transitions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class blockPuzzle_3:
    '''Stores all the stuff. You know what I mean.'''

    currentState = [[0 for x in range(3)] for y in range(3)]
    currentBlank = [-1, -1]

    def __init__(self, beginState, path = []):
        if check(self, beginState):
            self.currentState = [list(s) for s in beginState]
            self.path = path
        else:
            raise ValueError, 'Invalid initial puzzle.'

    def getState(self):
        a = []
        for row in self.currentState:
            a.append(tuple(row))
        return tuple(a)

    def getPath(self):
        return self.path

    def getDepth(self):
        return len(self.path)

########################


def move(self, move):
    '''Returns the state if you moved the blank space _move_'''
    #print self.currentBlank

    if not isValidMove(self, self.currentBlank, transitions, move):
        print 'invalid move'
        return

    nonBlankPlace = [self.currentBlank[0]-transitions[move][0],
                     self.currentBlank[1]-transitions[move][1]]
    nonBlankVal = self.currentState[nonBlankPlace[0]][nonBlankPlace[1]]
    #print nonBlankVal
    #quick replace

    self.currentState[nonBlankPlace[0]][nonBlankPlace[1]] = 0
    self.currentState[self.currentBlank[0]][self.currentBlank[1]] = \
                                                            nonBlankVal
    self.currentBlank[0] -= transitions[move][0]
    self.currentBlank[1] -= transitions[move][1]

    self.path.append(move)

def moveAndGet(self, movePlace):
    currentState = list(self.getState())
    newState = blockPuzzle_3(currentState, self.path[:])
    move(newState, movePlace)
    return newState

def check(puzzle, state):
    a = []
    for row in range(3):
        for element in range(3):
            if state[row][element] == 0:
                puzzle.currentBlank = [row, element]
            a.append(state[row][element])
    a.sort()
    if a == range(9):
        return True
    else:
        return False

def isValidMove(self, blankPlace, transitions, move):
    newY = blankPlace[0] - transitions[move][0]
    newX = blankPlace[1] - transitions[move][1]
    if newY < 0 or newY > 2 or \
       newX < 0 or newX > 2:
        return False
    else:
        return True


def expand(self, explored = set()):
    a = []
    for movePlace in range(4):
        if isValidMove(self, self.currentBlank, transitions, movePlace):
            newState = moveAndGet(self, movePlace)
            if newState.getState() not in explored:
                a.append(newState)
    return a


def show(self):
    for row in self.currentState:
        print row
    print '======='

def illustrateSolution(solution):
    puzzle = blockPuzzle_3(initState)
    for movement in solution:
        show(puzzle)
        move(puzzle, movement)
    show(puzzle)


goalState = ((1, 2, 3),
            (4, 5, 6),
            (7, 8, 0))


def spitOutStats(lenFrontier, lenExplored, lenPath):
    print 'Size of frontier: %i' % lenFrontier
    print 'Size of explored: %i' % lenExplored
    print 'Length of path: %i' % lenPath



####INFORMED ALGORITHMS

goalStateLookupTable = {0: (2, 2),
                        1: (0, 0),
                        2: (0, 1),
                        3: (0, 2),
                        4: (1, 0),
                        5: (1, 1),
                        6: (1, 2),
                        7: (2, 0),
                        8: (2, 1)}

#####code to generate 'goalStateLookupTable':
##goalStateLookupTable = {}
##for row in range(len(goalState)):
##    for element in range(len(goalState[row])):
##        goalStateLookupTable[goalState[row][element]] = (row, element)
#####

def h(state):
    '''The heuristic function. Return the sum of the manhattan distances
    of each block to their proper location.'''

    s = 0
    for row in range(3):
        for element in range(3):
            block = state[row][element]
            goalRow, goalCol = goalStateLookupTable[block]
            difRow = abs(row - goalRow)
            difCol = abs(element - goalCol)
            s += difRow + difCol
    return s

def greedyBestFirstSearch():
    initBlock = blockPuzzle_3(initState)
    initEval = h(initBlock.getState())
##    depth = -1
    explored = set()
    frontier = Queue.PriorityQueue()
    frontier.put((initEval, initBlock))

    currentHeuristic = 1000
    newHeuristic, currentNode = frontier.get()
    while currentNode.getState() != goalState:

##        currentDepth = currentNode.getDepth()
##        if currentDepth != depth:
##            depth = currentDepth
##            print 'Depth = %i' % depth
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
        for newNode in expand(currentNode, explored):
            frontier.put((h(newNode.getState()), newNode))
        explored.add(currentNode.getState())
##
##        if newHeuristic < currentHeuristic:
##            currentHeuristic = newHeuristic
##            print 'current Heuristic = %i' % currentHeuristic
##            print 'Depth = %i' % currentNode.getDepth()
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
##            print '============'

        if frontier.empty():
            print 'This puzzle is not solvable.'
            return
        
        newHeuristic, currentNode = frontier.get()

    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(frontier.qsize(), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()

def depthLimitedGreedySearch():
    initBlock = blockPuzzle_3(initState)
    initEval = h(initBlock.getState())
##    depth = -1
    explored = set()
    frontier = Queue.PriorityQueue()
    frontier.put((initEval, initBlock))

    currentHeuristic = 1000
    newHeuristic, currentNode = frontier.get()
    currentDepth = currentNode.getDepth()
    while currentNode.getState() != goalState:

        currentDepth = currentNode.getDepth()
        
##        currentDepth = currentNode.getDepth()
##        if currentDepth != depth:
##            depth = currentDepth
##            print 'Depth = %i' % depth
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
        if currentDepth < 31: #3-puzzles can be solved in at most 31 moves
            for newNode in expand(currentNode, explored):
                frontier.put((h(newNode.getState()), newNode))
        explored.add(currentNode.getState())
##
##        if newHeuristic < currentHeuristic:
##            currentHeuristic = newHeuristic
##            print 'current Heuristic = %i' % currentHeuristic
##            print 'Depth = %i' % currentNode.getDepth()
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
##            print '============'

        if frontier.empty():
            print 'This puzzle is not solvable.'
            return

        newHeuristic, currentNode = frontier.get()

    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(frontier.qsize(), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()
        

##### A-STAR TO THE RESCUE
def AStarSearch():
    initBlock = blockPuzzle_3(initState)
    explored = set()
    initHeuristic = h(initBlock.getState())
    frontier = Queue.PriorityQueue()
    frontier.put((initHeuristic, initBlock))
    depth = -1
    oldCombHeuristic = 0

    currentCombHeuristic, currentNode = frontier.get()
    while currentNode.getState() != goalState:
        
##        if currentCombHeuristic != oldCombHeuristic:
##            oldCombHeuristic = currentCombHeuristic
##            print 'current combined Heuristic = %i' % currentCombHeuristic
##            print 'Depth = %i' % currentNode.getDepth()
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
##            print '============'

        
        #f(n) = h(n) + g(n)
        #h(n) defined above, g(n) simply depth of node
        for newNode in expand(currentNode, explored):
            frontier.put((h(newNode.getState()) + newNode.getDepth(), newNode))

        explored.add(currentNode.getState())
        if frontier.empty():
            print 'This puzzle is not solvable.'
            return
        currentCombHeuristic, currentNode = frontier.get()
        
    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(frontier.qsize(), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()        


########################
def breadthFirstSearch():
    initBlock = blockPuzzle_3(initState)
    explored = set()
    frontier = Queue.Queue()
    frontier.put(initBlock)
##    depth = -1

    currentNode = frontier.get()
    while currentNode.getState() != goalState:
##        currentDepth = currentNode.getDepth()
##        if currentDepth != depth:
##            depth = currentDepth
##            print 'Depth = %i' % depth
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
        for newNode in expand(currentNode, explored):
            frontier.put(newNode)
        explored.add(currentNode.getState())

        if frontier.empty():
            print 'This puzzle is not solvable.'
            return
        currentNode = frontier.get()
    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(frontier.qsize(), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        solution = AStarSearch()
        print 'Usage: ./8BlockPuzzle.py [algorithm]'
    else:
        if sys.argv[1] == 'AStar':
            solution = AStarSearch()
        elif sys.argv[1] == 'BreadthFirst':
            solution = breadthFirstSearch()
        elif sys.argv[1] == 'Greedy':
            solution = greedyBestFirstSearch()
        elif sys.argv[1] == 'DepthLimitedGreedy':
            solution = depthLimitedGreedySearch()

