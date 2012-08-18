#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

#### Memoize function to use later
import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)
#####


#My family and I are going to be visiting the States to see a few colleges/
#universities, so I thought what better time to play around with TSP?
#Don't know what I'll try, but first up for sure is brute force, with
#O(n!) complexity. Here goes!


################################Data########################
#Destination places:
#Home = Toronto
#Cornell = Ithaca, NY
#Dartmouth = Hanover, NH
#Harvard = Cambridge, MA
#Yale = New Haven, CT
#Carnegie = Pittsburgh, PA
#Boston = Boston, MA
#Falls = Seneca Falls, NY

distances = (
    #Distances from Home
    (('Home', 'Cornell'), 397),
    (('Home', 'Harvard'), 881),
    (('Home', 'Yale'), 820),
##    (('Home', 'Carnegie'), 516),
    (('Home', 'Boston'), 886),
    (('Home', 'Falls'), 338),

    #Distances from Cornell
    (('Cornell', 'Harvard'), 530),
    (('Cornell', 'Yale'), 419),
##    (('Cornell', 'Carnegie'), 560),
    (('Cornell', 'Boston'), 533),
    (('Cornell', 'Falls'), 67),

    #Distances from Harvard
    (('Harvard', 'Yale'), 217),
##    (('Harvard', 'Carnegie'), 915),
    (('Harvard', 'Boston'), 5), #no joke
    (('Harvard', 'Falls'), 557),

    #Distances from Yale
##    (('Yale', 'Carnegie'), 722),
    (('Yale', 'Boston'), 222),
    (('Yale', 'Falls'), 502),

    #Distances from Carnegie
##    (('Carnegie', 'Boston'), 944),
##    (('Carnegie', 'Falls'), 523),

    #Distance from Boston
    (('Boston', 'Falls'), 560)
    )

allLocs = set()
for distance in distances:
    for endPoint in distance[0]:
        allLocs.add(endPoint)

cities = tuple(allLocs) #create an ordered list of the places for HK alg.

#since distances are the same both ways, I will store them in a table
#of key-value pairs where the key is a set containing the two destinations.
#Technically a frozenset, so it's hashable.
distanceTable = {}
for distanceComb in distances:
    distanceTable[frozenset(distanceComb[0])] = distanceComb[1]

#An easier way to access the data
def getDistance(loc1, loc2):
    '''Returns the distance between loc1 and loc2 according to the table.'''
    return distanceTable[frozenset((loc1, loc2))]

def getTotDist(sequence):
    '''Returns the total distance of a proposed sequence.'''
    s = 0
    for i in range(len(sequence)-1):
        s += getDistance(sequence[i], sequence[i+1])
    return s


###################################Algorithms########################

####Brute Force Method
def bruteForce():
    '''The brute force method.'''
    #Thank god for itertools.permutations. I would have had (and still don't)
    #have any clue how to find all permutations of a list.
    import itertools
    #Find every permutation of the places we visit.
    sequences = list(itertools.permutations(cities))
    #Remember to start and end at home.
    #Each sequence in sequences stores a list as follows:
    #[Total distance, [list of places to go in order]]
    for i in range(len(sequences)):
        currentSeq = list(sequences[i])
        currentSeq.append(currentSeq[0]) #make cyclical
        sequences[i] = [-1, currentSeq]
    #Go through each sequence and update the total distance for each.
    for i in range(len(sequences)):
        sequences[i][0] = getTotDist(sequences[i][1])
    #Sort by order of least distance.
    sequences.sort()
    return sequences[0]



####Held-Karp Dynamic Programming Method
# I have Held/Karp's 1962 paper on "A Dynamic Programming Approach To
# Sequencing Problems," but don't really understand it.
# (You can find it through TPL on JSTOR if you want to read it.)
# Oh well. What's the worst that can happen?
# O(n^2*2^n), here I come!

# Equation 5 in the paper reads as follows:
# (5) a) (n(S) = 1):    C({l}, l) = a_1l,   for any l.
#     b) (n(S) > 1):    C(S, l) = min_mϵs-l [C(S-l, m) + a_ml].
# In which S is a perfect subset of the integers from {2, 3, ..., n}
# and l ϵ S, and C(S, l) denotes the minimum cost of starting from
# city one and visiting all cities in the set S, terminating at city l.
# Note that because Python is zero-indexed, S is actually from {1, ..., n-1}

@memoized
def Eq5HKD(S, el):

    # Each return returns the minimum distance of starting at
    # city 0 and going through all cities in the subset S, as well as
    # the number of the city determined to be the minimum distance from el.
    
    #5 a)
    if len(S) == 1:
        return getDistance(cities[0], cities[el]), [0]
    #5 b)
    elif len(S) > 1:
        newS = set(S.copy())
        newS.remove(el)
        minM = 100000000 #some really big number
        for m in newS:
            newC = Eq5HKD(frozenset(newS), m)
            newM = newC[0] + getDistance(cities[m], cities[el])
            if newM < minM:
                minM = newM
                path = [m] + newC[1]
        return minM, path
        

def HeldKarpDynamic():
    '''The method as described in Held and Karp's 1962 paper.
    Coincidentally, also the one referenced by xkcd.'''
    subCities = set(range(1, len(cities)))

    # Equation 6 in the paper reads as follows:
    # (6)   c = min_lϵ{2, 3, ..., n} [C({2, 3, ..., n}, l) + a_l1].
    # Note again that we must zero-index things.

    minC = 100000000 #some really big number
    for el in subCities:
        i = Eq5HKD(frozenset(subCities), el)
        newC = i[0] + getDistance(cities[el], cities[0])
        if newC < minC:
            minC = newC
            path = [0, el] + i[1]
    solution = [cities[x] for x in path]
    return minC, solution
    
#############################Main##########################
if __name__ == '__main__':
    solution = HeldKarpDynamic()
    print('Shortest route is {0} with total distance {1}km.'\
    .format(solution[1], solution[0]))
    
    solution = bruteForce()
    print('Shortest route is {0} with total distance {1}km.'\
    .format(solution[1], solution[0]))
