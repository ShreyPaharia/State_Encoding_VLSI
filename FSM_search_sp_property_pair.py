#!/usr/bin/python
import math
import numpy as np
import itertools
import sys
import itertools

def partition_intersect (p1, p2):
    return frozenset ([b1.intersection (b2) for b1 in p1 for b2 in p2 if 0 != len (b1.intersection (b2))])


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
    print("\nNEW PARTITION PAIRS FOUND FOR THE ABOVE FSM:")
    lattice = set ()
    lattice.add (frozenset ([frozenset (range (N))]))
    lattice.add (frozenset ([frozenset ([i]) for i in range (N)]))
    for statePair in itertools.combinations (range (N), 2):
        p = getPartition (frozenset (statePair))
        if p not in lattice:
            lattice.add (p)
            print ('# New partition for pair ' + str (statePair) + " : " + str (p)+"\n")
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
    print ("\nLATTICE FOR THE ABOVE FSM :")
    for p in lattice:
        print ("         " + str (p))
    print("\n")

    return lattice

def intersect (p1,p2,assigned_states1,assigned_states2,N):
    a = [0]*N
    for i in range(len(p1)):
        for j in range(len(p2)):
            intersect_lists =list(p1)[i].intersection (list(p2)[j])
            if(len(intersect_lists)):
                a[list(intersect_lists)[0]] = assigned_states1[i] + assigned_states2[j]
    return a

def state_assignment(p1,p2):
    noBits1 = math.ceil(math.log(len(p1),2))
    noBits2 = math.ceil(math.log(len(p2),2))
    encoding_list1 = list(itertools.product([False, True], repeat=int(noBits1))) 
    encoding_list2 = list(itertools.product([False, True], repeat=int(noBits2)))
    encoding_list  = list(itertools.product([False, True], repeat=int(noBits)))
    assigned_states1 = [0]*len(p1)
    assigned_states2 = [0]*len(p2)

    for j1 in range(len(p1)):
        assigned_states1[j1] = encoding_list1[j1]

    for j2 in range(len(p2)):
        assigned_states2[j2] = encoding_list2[j2]

    # print("assigned_states1")
    # print(assigned_states1)

    # print("assigned_states2")
    # print(assigned_states2)

    # print("intersect(p1,p2)")

    final = intersect(p1,p2,assigned_states1,assigned_states2,N)
    return final

def print_state_assignment(state_assignment):

    #encoding_print used to store the list of encodings for each state
    encoding_print = []

    for encoding in state_assignment:
        #used to append either 1 or 0 according to the boolean values in encoding
        encoding_print_element =''
        for bit in encoding:
            if(bit):
                encoding_print_element+='1'
            else:
                encoding_print_element+='0'

        encoding_print.append(encoding_print_element)

    for i in range(len(state_assignment)):
        print("S"+str(i)+" : "+encoding_print[i])


#tt = [(3,2),(5,2),(4,1),(1,4),(0,3),(2,3)]     # Example in figure 8.18
tt = [(0,0),(1,2),(4,3),(5,2),(1,2),(1,3)]     # Example in figure 8.26, with addition of isolated 0 state for easy indexing.
N = len (tt)
noBits = math.ceil(math.log(N,2))

# Find partition pairs with substitution property :

spPairs = set ()
lattice = getLattice ()
sp_pair_found = False

for p1 in lattice:
    if N == len (p1) or 1 == len (p1):
        continue
    for p2 in lattice:
        if N == len (p2) or 1 == len (p2):
            continue
        p1_intersect_p2 = partition_intersect (p1, p2)
        if N == len (p1_intersect_p2):
            spPair = frozenset ([p1, p2])
            if spPair not in spPairs:
                sp_pair_found=True

                spPairs.add (spPair)
                print ("FOUND A NONTRIVIAL PARTITION PAIR WITH SUBSTITUTION PROPERTY:")
                print ("                     " + str (p1))
                print ("                     " + str (p2))
                print("\n\n")

                state_assignment_try = state_assignment(p1,p2)
                

                print("STATE ASSIGNMENT ACCORDING TO THIS PARTITION PAIR")
                print_state_assignment(state_assignment_try)
                print("\n\n")

if sp_pair_found == False:
    print("NO NONTRIVIAL PARTITION PAIR WITH SUBSTITUTION PROPERTY FOUND")

