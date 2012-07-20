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
            (9, 10,11, 12),
            (13, 14, 15, 0))


########################
def depthFirstSearch():
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
    return currentNode.getPath()



if __name__ == '__main__':
    solution = depthFirstSearch()
    #illustrateSolution(solution)

