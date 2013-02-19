#!/bin/python

selected_cells = []
black = []
white = []
dead = []

def findCell(player, board):
	global selected_cells
	global dead

	adjacent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	opponent = 'w' if player == 'b' else 'b'

	selected = False
	for cell in dead:

		tmpBoard = list(board)
		tmpBoard[cell[0]] = tmpBoard[cell[0]][0:cell[1]] + player + tmpBoard[cell[0]][cell[1]+1:]

		#print "Examining {0}".format(cell)
		player_cells = 0
		opponent_cells = 0

		for adj in adjacent:
			adjPos = (cell[0]+adj[0], cell[1]+adj[1])
			if adjPos[0] >= 0 and adjPos[0] < len(tmpBoard) and adjPos[1] >= 0 and adjPos[1] < len(tmpBoard[i]):
				if tmpBoard[adjPos[0]][adjPos[1]] == player:
					player_cells += 1
				elif tmpBoard[adjPos[0]][adjPos[1]] == opponent:
					opponent_cells += 1
	
		sum_cells = player_cells + opponent_cells
		
		#Start of conditions for selection
		cluster = []
		getCluster(tmpBoard, cell, cluster)
		
		if opponent_cells > 2 and player_cells == 0  and sum_cells < 4:
			selected_cells.append(cell)
			selected = True
			break
		
		if player_cells > 0  and sum_cells < 3:
			if len(cluster) < 7:
				selected_cells.append(cell)
				selected = True
				break

		#End of conditions for selection	

	if not selected:
		minSize = 10000
		selectedCell = (-1,-1)
		for cell in dead:
			tmpBoard = list(board)
			tmpBoard[cell[0]] = tmpBoard[cell[0]][0:cell[1]] + player + tmpBoard[cell[0]][cell[1]+1:]
			cluster = []
			getCluster(tmpBoard, cell, cluster)
			if len(cluster) < minSize:
				minSize = len(cluster)
				selectedCell = cell
		
		selected_cells.append(selectedCell)

def checkNextMove(player, board):
	global black
	global white
	maxScore = 0
	pos = (-1,-1)
	findCell(player,board)
	for cell in selected_cells:
		#simulate(player, newBoard, cell)
		#count(newBoard)
		score = len(black) if player == 'b' else len(white)
		#print "Score for {0} : {1}".format(cell,score)
		if score > maxScore or pos == (-1,-1):
			maxScore = score
			pos = cell
	
	#printBoard(newBoard) 
	
	return pos

def printBoard(board):
	print "----- Start of board -----"
	for r in board:
		print r
	print "----- End -----"

def simulate(player, board, pos):
	board[pos[0]] = board[pos[0]][0:pos[1]] + player + board[pos[0]][pos[1]+1:]
	flipCluster(board, pos, 3)


def getCluster(board, pos, cluster):
	adjacent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	#print "pos: {0}, val: {1}".format(pos,board[pos[0]][pos[1]])
	if board[pos[0]][pos[1]] == '-':
		return
	else:
		cluster.append(pos)

	for adj in adjacent:
		adjPos = (pos[0]+adj[0],pos[1]+adj[1])
		if adjPos in cluster:
			continue
		if adjPos[0] >= 0 and adjPos[0] < len(board) and adjPos[1] >= 0 and adjPos[1] < len(board[i]):
			adjCell = board[adjPos[0]][adjPos[1]]
			if adjCell ==  board[cluster[0][0]][cluster[0][1]]:
				getCluster(board, adjPos, cluster)


def flipCluster(board, pos, recurseDepth):
	if recurseDepth < 0:
		return
	black,white = 0,0
	adjacent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
	for adj in adjacent:
		adjPos = (pos[0]+adj[0],pos[1]+adj[1])
		if adjPos[0] >= 0 and adjPos[0] < len(board) and adjPos[1] >= 0 and adjPos[1] < len(board[i]):
			adjCell = board[adjPos[0]][adjPos[1]]
			if adjCell == 'b':
				black += 1
			elif adjCell == 'w':
				white += 1
			flipCluster(board, adjPos, recurseDepth-1)

	if (black+white) > 3 or (black+white) < 3:
		board[pos[0]] = board[pos[0]][0:pos[1]] + '-' + board[pos[0]][pos[1]+1:]
	else:
		p = 'b' if (black > white) else 'w'
		board[pos[0]] = board[pos[0]][0:pos[1]] + p + board[pos[0]][pos[1]+1:]


def count(board):
	global black
	global white
	global dead

	black,white,dead = [],[],[]

	for i in xrange(0, len(board)):
		for j in xrange(0, len(board[i])):
			if board[i][j] == 'w':
				white.append((i,j)) 
			elif board[i][j] == 'b':
				black.append((i,j))
			else:
				dead.append((i,j))
		

# Head ends here

def nextMove(player,board):
	count(board)
	pos = checkNextMove(player, board)
	return pos

# Tail starts here
player = raw_input()
board = []
for i in xrange(0, 29):
	board.append(raw_input())

a,b = nextMove(player,board)
print a,b
