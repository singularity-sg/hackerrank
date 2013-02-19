#!/usr/bin/python

import math
import random

# Head ends here

def calculateCost(pos, dirtySpot):
    return math.fabs(pos[0]-dirtySpot[0]) + math.fabs(pos[1]-dirtySpot[1])

def printMove(pos, dirty):
    if dirty[0] < pos[0] and pos[0] > 0:
        print "UP"
    elif dirty[0] > pos[0] and pos[1] < 4:
        print "DOWN"
    elif dirty[1] < pos[1] and pos[1] > 0:
        print "LEFT"
    elif dirty[1] > pos[1] and pos[1] < 4:
        print "RIGHT"
    else:
        print "CLEAN"

def explore(pos):
    possible = []
    for i in range(pos[0]-1, pos[0]+1):
        for j in range(pos[1]-1, pos[1]+1):
            if i >= 0 and i <= 4 and j >= 0 and j <= 4:
                if not (i == posx and j == posy):
                    possible.append((i,j))
    
    new_pos = random.choice(possible)
    
    printMove(pos, new_pos)

def next_move(posx, posy, board):
    dirty = []
   
    for i in range(posx-1, posx+1):
        for j in range(posy-1, posy+1):
            if i >= 0 and i <= 4 and j >= 0 and j <= 4:
                if not (i == posx and j == posy):
                    if board[i][j] == 'd':
                        dirty.append((i,j,calculateCost((posx,posy),(i,j))))
                    
    dirty.sort(key=lambda tup: tup[2])  
   
    if len(dirty) > 0:
        printMove((posx,posy),(dirty[0]))
    else:
        explore((posx,posy))
    
if __name__ == "__main__":
    pos = [int(i) for i in raw_input().strip().split()]
    board = [[j for j in raw_input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)

