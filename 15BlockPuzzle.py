#!/usr/bin/env python
#let's try and implement that block puzzle. 15 blocks this time.

initState = [[2, 12, 11, 14],
             [6, 15, 10, 5],
             [3, 0, 9, 13],
             [8, 7, 1, 4]]

actions = ['L', 'R', 'U', 'D']
transitions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class blockPuzzle_4:
    '''Stores all the stuff. You know what I mean.'''

    currentState = [[0 for x in range(4)] for y in range(4)]
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
    newState = blockPuzzle_4(currentState, self.path[:])
    move(newState, movePlace)
    return newState

def check(puzzle, state):
    a = []
    for row in range(4):
        for element in range(4):
            if state[row][element] == 0:
                puzzle.currentBlank = [row, element]
            a.append(state[row][element])
    a.sort()
    if a == range(16):
        return True
    else:
        return False

def isValidMove(self, blankPlace, transitions, move):
    newY = blankPlace[0] - transitions[move][0]
    newX = blankPlace[1] - transitions[move][1]
    if newY < 0 or newY > 3 or \
       newX < 0 or newX > 3:
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
    puzzle = blockPuzzle_4(initState)
    for movement in solution:
        show(puzzle)
        move(puzzle, movement)
    show(puzzle)


goalState = ((1, 2, 3, 4),
            (5, 6, 7, 8),
            (9, 10, 11, 12),
            (13, 14, 15, 0))

def spitOutStats(lenFrontier, lenExplored, lenPath):
    print 'Size of frontier: %i' % lenFrontier
    print 'Size of explored: %i' % lenExplored
    print 'Length of path: %i' % lenPath


####################### INFORMED SEARCH STUFFS

goalStateLookupTable = {0: (3, 3),
                        1: (0, 0),
                        2: (0, 1),
                        3: (0, 2),
                        4: (0, 3),
                        5: (1, 0),
                        6: (1, 1),
                        7: (1, 2),
                        8: (1, 3),
                        9: (2, 0),
                        10: (2, 1),
                        11: (2, 2),
                        12: (2, 3),
                        13: (3, 0),
                        14: (3, 1),
                        15: (3, 2)}

def h(state):
    '''The heuristic function. Return the sum of the manhattan distances
    of each block to their proper location.'''

    s = 0
    for row in range(len(state)):
        for element in range(len(state[row])):
            block = state[row][element]
            goalRow, goalCol = goalStateLookupTable[block]
            difRow = abs(row - goalRow)
            difCol = abs(element - goalCol)
            s += difRow + difCol
    return s

def greedyBestFirstSearch():
    initBlock = blockPuzzle_4(initState)
    initEval = h(initBlock.getState())
##    depth = -1
    explored = set()
    frontier = [(initEval, initBlock)]

    currentHeuristic = 1000
    newHeuristic, currentNode = frontier.pop()
    while currentNode.getState() != goalState:
        
##        currentDepth = currentNode.getDepth()
##        if currentDepth != depth:
##            depth = currentDepth
##            print 'Depth = %i' % depth
##            print 'Size of explored = %i' % len(explored)
##            print 'Size of frontier = %i' % len(frontier)
            
        frontier.extend([(h(x.getState()),
                          x) for x in expand(currentNode, explored)])
        explored.add(currentNode.getState())
        
        if newHeuristic < currentHeuristic:
            currentHeuristic = newHeuristic
            print 'current Heuristic = %i' % currentHeuristic
            print 'Depth = %i' % currentNode.getDepth()
            print 'Size of explored = %i' % len(explored)
            print 'Size of frontier = %i' % len(frontier)
            print '============'

        if len(frontier) == 0:
            print 'This puzzle is not solvable.'
            return
        
        frontier.sort(reverse = True)
        newHeuristic, currentNode = frontier.pop()
        
    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(len(frontier), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()


##### A-STAR TO THE RESCUE
def AStarSearch():
    initBlock = blockPuzzle_4(initState)
    explored = set()
    initHeuristic = h(initBlock.getState())
    frontier = [(initHeuristic, initBlock)]
    depth = -1
    oldCombHeuristic = 0

    currentCombHeuristic, currentNode = frontier.pop()
    while currentNode.getState() != goalState:
        
        if abs(currentCombHeuristic - oldCombHeuristic) > 3:
            oldCombHeuristic = currentCombHeuristic
            print 'current combined Heuristic = %i' % currentCombHeuristic
            print 'Depth = %i' % currentNode.getDepth()
            print 'Size of explored = %i' % len(explored)
            print 'Size of frontier = %i' % len(frontier)
            print '============'

        
        #f(n) = h(n) + g(n)
        #h(n) defined above, g(n) simply depth of node
        frontier.extend([(h(x.getState())+x.getDepth(), x) for x
                         in expand(currentNode, explored)])
        frontier.sort(reverse = True)
        explored.add(currentNode.getState())
        if len(frontier) == 0:
            print 'This puzzle is not solvable.'
            return
        currentCombHeuristic, currentNode = frontier.pop()
        
    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(len(frontier), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()        


########################
def breadthFirstSearch():
    from collections import deque
    initBlock = blockPuzzle_4(initState)
    explored = set()
    frontier = deque([initBlock])
    depth = -1

    currentNode = frontier.popleft()
    while currentNode.getState() != goalState:
        currentDepth = currentNode.getDepth()
        if currentDepth != depth:
            depth = currentDepth
            print 'Depth = %i' % depth
            print 'Size of explored = %i' % len(explored)
            print 'Size of frontier = %i' % len(frontier)
        frontier.extend(expand(currentNode, explored))
        explored.add(currentNode.getState())
        #print 'frontier = ', frontier
        if len(frontier) == 0:
            print 'This puzzle is not solvable.'
            return
        currentNode = frontier.popleft()
    for movement in currentNode.getPath():
        print actions[movement],
    print
    spitOutStats(len(frontier), len(explored), len(currentNode.getPath()))
    return currentNode.getPath()



if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        solution = AStarSearch()
    if sys.argv[1] == 'AStar':
        solution = AStarSearch()
    elif sys.argv[1] == 'BreadthFirst':
        solution = breadthFirstSearch()
    elif sys.argv[1] == 'Greedy':
        solution = greedyBestFirstSearch()
    else:
        print 'Usage: ./15BlockPuzzle.py [algorithm]'
