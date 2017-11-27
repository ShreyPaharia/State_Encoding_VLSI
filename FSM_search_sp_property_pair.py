#!/usr/bin/python

import sys
import itertools

def partition_intersect (p1, p2):
    intersect = frozenset ([b1.intersection (b2) for b1 in p1 for b2 in p2 if 0 != len (b1.intersection (b2))])
    return intersect

def partition_union (p1, p2):
    p1_union_p2 = frozenset ([b1 for b1 in p1])
    for b2 in p2:
        p1_union_p2 = frozenset (filter (b2.isdisjoint, p1_union_p2) + [reduce (frozenset.union, filter (lambda x: not b2.isdisjoint (x), p1_union_p2))])
    return p1_union_p2

def mergeBlocks (p, b):
    result = set ()
    mergedblock = frozenset ()
    for b2 in p:
        if True == b2.isdisjoint (b):
            result.add (b2)
        else:
            mergedblock = mergedblock.union (b2)
    if 0 != len (mergedblock):
        result.add (mergedblock)
    return frozenset (result)

def getNextStateBlocks (b):
    blocks = dict ()
    for s in b:
        for inp in range (len (tt[s])):
            if inp not in blocks:
                blocks[inp] = frozenset ()
            blocks[inp] = blocks[inp].union (frozenset ([tt[s][inp]]))
    return {blocks[inp] for inp in blocks}

def getPartition (b12):
    "Get a partition such that states in b12 are in one block"
    p = {frozenset ([i]) for i in range (N)}
    p = mergeBlocks (p, b12)
    changeHappened = True
    while changeHappened:
        changeHappened = False
        for b in p:
            for nsb in getNextStateBlocks (b):
                if 1 != [b2.isdisjoint (nsb) for b2 in p].count (False):
                    changeHappened = True
                    p = mergeBlocks (p, nsb)
                    break
            if changeHappened:
                break
    return p

def getLattice ():
    "Return a lattice of partitions having SP property"
    lattice = set ()
    lattice.add (frozenset ([frozenset (range (N))]))
    lattice.add (frozenset ([frozenset ([i]) for i in range (N)]))

    for statePair in itertools.combinations (range (N), 2):
        print("statepair")
        print(statePair)
        p = getPartition (frozenset (statePair))
        print("p")
        print(p)

        if p not in lattice:
            lattice.add (p)
            print ('# New partition for pair ' + str (statePair) + " : " + str (p))
    changeHappened = True
    while changeHappened:
        changeHappened = False
        for p1 in lattice:
            for p2 in lattice:
                p1_intersect_p2 = partition_intersect (p1, p2)
                if p1_intersect_p2 not in lattice:
                    lattice.add (p1_intersect_p2)
                    changeHappened = True
                p1_union_p2 = partition_union (p1, p2)
                if p1_union_p2 not in lattice:
                    lattice.add (p1_union_p2)
                    changeHappened = True
                if changeHappened:
                    break
            if changeHappened:
                break
    
    print ("Lattice :")
    for p in lattice:
        print (" " + str (p))
    return lattice


tt = [(3,2),(5,2),(4,1),(1,4),(0,3),(2,3)]     # Example in figure 8.18
# tt = [(0,0),(1,2),(4,3),(5,2),(1,2),(1,3)]     # Example in figure 8.26, with addition of isolated 0 state for easy indexing.
N = len (tt)

# Find partition pairs with substitution property :
spPairs = set ()
lattice = getLattice ()
for p1 in lattice:
    if N == len (p1) or 1 == len (p1):
        continue
    for p2 in lattice:
        if N == len (p2) or 1 == len (p2):
            continue
        p1_intersect_p2 = partition_intersect (p1, p2)
        print("p1_intersect_p2")
        print(p1_intersect_p2)
        if N == len (p1_intersect_p2):
            spPair = frozenset ([p1, p2])
            if spPair not in spPairs:
                spPairs.add (spPair)
                print ("Found a nontrivial partition pair with substitution property :")
                print ("   " + str (p1))
                print ("   " + str (p2))