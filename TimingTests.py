#!/usr/bin/env python
#timing tests
import timeit
import BlockPuzzle8

AStarSearch8 = timeit.timeit('BlockPuzzle8.AStarSearch()',
                     'from __main__ import BlockPuzzle8',
                     number = 10)

breadthFirstSearch8 = timeit.timeit('BlockPuzzle8.breadthFirstSearch()',
                                    'from __main__ import BlockPuzzle8',
                                    number = 10)

greedy8 = timeit.timeit('BlockPuzzle8.greedyBestFirstSearch()',
                        'from __main__ import BlockPuzzle8',
                        number = 10)

depthLimitedGreedy8 = timeit.timeit('BlockPuzzle8.depthLimitedGreedySearch()',
                                    'from __main__ import BlockPuzzle8',
                                    number = 10)


print 'A* on 8 puzzle: %f' % AStarSearch8
#Non-priority queue: 6.221501

print 'Breadth-first search on 8 puzzle: %f' % breadthFirstSearch8
#Non-priority queue: 58.277133

print 'Greedy best-first search on 8 puzzle: %f' % greedy8
#Non-priority queue: 2.396569

print 'Depth-limited greedy search on 8 puzzle: %f' % depthLimitedGreedy8
#Non-priority queue: 243.450213
#wow. That's not very impressive. There goes my genius...
