#!/usr/bin/env python
#let's try and implement that block puzzle.


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
        return self.currentState

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


goalState = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]]


########################
def depthFirstSearch():
    from collections import deque
    initBlock = blockPuzzle_3([[7, 2, 4],
                                [5, 0, 6],
                                [8, 3, 1]],
                              [])
    explored = []
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
        explored.append(currentNode.getState())
        #print 'frontier = ', frontier
        currentNode = frontier.popleft()
    for movement in currentNode.getPath():
        print actions[movement],
    return currentNode.getPath()


if __name__ == '__main__':
    initBlock = blockPuzzle_3([[7, 2, 4],
                                [0, 5, 6],
                                [8, 3, 1]],
                              [])
    depthFirstSearch()
##    stuff = [initBlock.getState()]
##    show(initBlock)
##    b = expand(initBlock, stuff)
##    for i in b:
##        show(i)
##        stuff.append(i.getState())


