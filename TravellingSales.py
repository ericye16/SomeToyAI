#!/usr/bin/env python

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



###################################Algorithm########################
def bruteForce():
    '''The brute force method.'''
    pass #TODO: figure this out
