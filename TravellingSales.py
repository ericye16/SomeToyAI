#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    (('Home', 'Carnegie'), 516),
    (('Home', 'Boston'), 886),
    (('Home', 'Falls'), 338),

    #Distances from Cornell
    (('Cornell', 'Harvard'), 530),
    (('Cornell', 'Yale'), 419),
    (('Cornell', 'Carnegie'), 560),
    (('Cornell', 'Boston'), 533),
    (('Cornell', 'Falls'), 67),

    #Distances from Harvard
    (('Harvard', 'Yale'), 217),
    (('Harvard', 'Carnegie'), 915),
    (('Harvard', 'Boston'), 5), #no joke
    (('Harvard', 'Falls'), 557),

    #Distances from Yale
    (('Yale', 'Carnegie'), 722),
    (('Yale', 'Boston'), 222),
    (('Yale', 'Falls'), 502),

    #Distances from Carnegie
    (('Carnegie', 'Boston'), 944),
    (('Carnegie', 'Falls'), 523),

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
    cities = allLocs.copy()
    cities.remove('Home')
    #Find every permutation of the places we visit.
    sequences = list(itertools.permutations(cities))
    #Remember to start and end at home.
    #Each sequence in sequences stores a list as follows:
    #[Total distance, [list of places to go in order]]
    for i in range(len(sequences)):
        sequences[i] = [-1, ['Home'] + list(sequences[i]) + ['Home']]
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
#     b) (n(S) > 1):    C(C, l) = min_mϵs-l [C(S-l, m) + a_ml].
# In which S is a perfect subset of the integers from {2, 3, ..., n}
# and l ϵ S, and C(S, l) denotes the minimum cost of starting from
# city one and visiting all cities in the set S, terminating at city l.
# Note that because Python is zero-indexed, S is actually from {1, ..., n-1}

def Eq5HKD(S, l):
    #5 a)
    if len(S) == 1:
        return getDistance(cities[0], cities[l])
    #5 b)
    elif len(S) > 1:
        newS = S[:]
        newS.remove(l)
        minM = 100000000 #some really big number
        for m in newS:
            newM = Eq5HKD(newS, m) + getDistance(cities[m], cities[0])
            if newM < minM:
                minM = newM
        return minM
        

def HeldKarpDynamic():
    '''The method as described in Held and Karp's 1962 paper.
    Coincidentally, also the one referenced by xkcd.'''
    subCities = range(1, len(cities))
    
    # Held and Karp's paper states that we perform two phases of computation:
    # In phase one, we determine the optimum cost (distance.)
    # In phase two, we find the permutation that matches that cost.
    # Yes, there are probably some optimizations that can be made but
    # I'm trying to implement this verbatim(-ish) from the paper.

    # Equation 6 in the paper reads as follows:
    # (6)   c = min_lϵ{2, 3, ..., n} [C({2, 3, ..., n}, l) + a_l1].
    # Note again that we must zero-index things.

    minC = 100000000 #some really big number
    for l in subCities:
        newC = Eq5HKD(subCities, l) + getDistance(cities[l], cities[0])
        if newC < minC:
            minC = newC
    print minC

    # At this point, the minimum cost should be in 'minC.'
    # However, I don't think the triangle inequality is held in our data,
    # so this may not work so well.

    # Currently, minC is 2573, which isn't even in the table of solutions
    # From the brute force method. This suggests a bug as opposed to
    # a non-optimal algorithm.



#############################Main##########################
if __name__ == '__main__':
    solution = bruteForce()
    print 'Shortest route is {0} with total distance {1}km.'.format(solution[1],
                                                                  solution[0])
