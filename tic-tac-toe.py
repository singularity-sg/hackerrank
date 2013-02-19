#!/bin/python
import random

# Check if first step is made
def firstMove(board):
	for i in range(0,3):
		for j in range(0,3):
			if board[i][j] != '_':
				return 0
	return 1

def printCenter(player, board):
	samples = [(1,1)]
	return choose(samples, board)

def printCorner(player, board):
	samples = [(0,0),(0,2),(2,0),(2,2)]
	return choose(samples, board)

def printSide(player, board):
	samples = [(0,1),(1,0),(1,2),(2,1)]
	return choose(samples, board)

def isOneOfThese(player, samples, board):
	for sample in samples:
		if board[sample[0]][sample[1]] == player:
			return 1
	return 0		

def choose(samples, board):
	while(len(samples) > 0):
		selected = samples.pop(random.randrange(0,len(samples)))
		if board[selected[0]][selected[1]] == '_':
			print "{0} {1}".format(selected[0],selected[1])
			return 1
			break
	else:
		return 0

def pick(player, board):
	opponent = 'O' if (player == 'X') else 'X'
	winning_samples = ((0,0),(0,1),(0,2)),((1,0),(1,1),(1,2)),((2,0),(2,1),(2,2)),((0,0),(1,0),(2,0)),((0,1),(1,1),(2,1)),((0,2),(1,2),(2,2)),((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0))

	for sample in winning_samples:
		if checkWinner(sample,player,board):
			return	
        
	for sample in winning_samples:	
		if blockOpponent(sample,player,board):
			return

	else:
		if isOneOfThese(opponent, ((0,0),(0,2),(2,0),(2,2)), board):
			if not printCenter(player, board):
				if not printCorner(player, board):
					printSide(player,board)
		elif not printCorner(player, board):
			if not printCenter(player, board):
				printSide(player, board)
			

def checkWinner(sample, player, board):
	return go(sample, player, board)

def blockOpponent(sample, player, board):
	if player == 'X':
		return go(sample, 'O', board)
	else:
		return go(sample, 'X', board)
	
def go(sample,player,board):	
	a = board[sample[0][0]][sample[0][1]]
	b = board[sample[1][0]][sample[1][1]]
	c = board[sample[2][0]][sample[2][1]]
	if a == player and b == player and c == '_':
		print "{0} {1}".format(sample[2][0],sample[2][1])
		return 1
	if a == player and c == player and b == '_':
		print "{0} {1}".format(sample[1][0],sample[1][1])
		return 1
	if b == player and c == player and a == '_':
		print "{0} {1}".format(sample[0][0],sample[0][1])
		return 1
	return 0
		

# Complete the function below to print 2 integers separated by a single space which will be your next move 
def nextMove(player,board):
	if firstMove(board):
		printCorner(player, board)
	else:
		pick(player, board)
				

#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()

#Read the board now. The board is a 3x3 array filled with X, O or _.
board = []
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player,board);  
