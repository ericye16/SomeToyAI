#!/usr/bin/env python
#let's try and implement that block puzzle.

class blockPuzzle_3:
    '''Stores all the stuff. You know what I mean.'''

    actions = ['L', 'R', 'U', 'D']
    transitions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    currentState = [[0 for x in range(3)] for y in range(3)]
    currentBlank = [-1, -1]

    def __init__(self, beginState, path = []):
        if self.check(beginState):
            self.currentState = [list(s) for s in beginState]
            self.path = path
        else:
            raise ValueError, 'Invalid initial puzzle.'

    def check(self, state):
        a = []
        for row in range(3):
            for element in range(3):
                if state[row][element] == 0:
                    self.currentBlank = [row, element]
                a.append(state[row][element])
        a.sort()
        if a == range(9):
            return True
        else:
            return False

    def move(self, move):
        '''Returns the state if you moved the blank space _move_'''
        #print self.currentBlank

        if not self.isValidMove(self.currentBlank, self.transitions, move):
            print 'invalid move'
            return
        
        nonBlankPlace = [self.currentBlank[0]-self.transitions[move][0],
                         self.currentBlank[1]-self.transitions[move][1]]
        nonBlankVal = self.currentState[nonBlankPlace[0]][nonBlankPlace[1]]
        #print nonBlankVal
        #quick replace
        
        self.currentState[nonBlankPlace[0]][nonBlankPlace[1]] = 0
        self.currentState[self.currentBlank[0]][self.currentBlank[1]] = \
                                                                nonBlankVal
        self.currentBlank[0] -= self.transitions[move][0]
        self.currentBlank[1] -= self.transitions[move][1]

        self.path.append(move)

    def show(self):
        for row in self.currentState:
            print row
        print '======='

    def isValidMove(self, blankPlace, transitions, move):
        newY = blankPlace[0] - transitions[move][0]
        newX = blankPlace[1] - transitions[move][1]
        if newY < 0 or newY > 2 or \
           newX < 0 or newX > 2:
            return False
        else:
            return True

    def moveAndGet(self, move):
        currentState = list(self.getState())
        newState = blockPuzzle_3(currentState, self.path[:])
        newState.move(move)
        return newState

    def getState(self):
        return self.currentState

    def getPath(self):
        return self.path

    def getDepth(self):
        return len(self.path)

    def expand(self, explored = set()):
        a = []
        for move in range(4):
            #print move
            if self.isValidMove(self.currentBlank, self.transitions, move):
                #self.show()
                newState = self.moveAndGet(move)
                if newState.getState not in explored:
                    #newState.show()
                    a.append(newState)
                    #newState.show()
                
        return a


########################



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
    explored = set()
    frontier = deque([initBlock])
    depth = -1
    
    currentNode = frontier.popleft()
    while currentNode.getState != goalState:
        currentDepth = currentNode.getDepth()
        if currentDepth != depth:
            depth = currentDepth
            print 'Depth = %i' % depth
        frontier.extend(currentNode.expand(explored))
        explored.add(currentNode.getState)
        #print 'frontier = ', frontier
        currentNode = frontier.popleft()
    print currentNode.getPath()
    
    
if __name__ == '__main__':
    initBlock = blockPuzzle_3([[7, 2, 4],
                                [0, 5, 6],
                                [8, 3, 1]],
                              [])
    depthFirstSearch()

