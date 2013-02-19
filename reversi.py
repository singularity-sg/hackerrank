#!/usr/bin/python

#Simulate 2 steps ahead to get the maximum points
def simulateMove(player, board, pos, myPoints):
   opponent = 'B' if player == 'W' else 'W'
   myBoard = list(board)
   totalOppPts = 0
   totalMyPts = myPoints

   #Simulate my step
   flipBoard(player, myBoard, pos)

   #Simulate opponent step
   oppPos,oppPts = calculateMaxPoints(opponent, myBoard)
   totalOppPts += oppPts
   flipBoard(opponent, myBoard, oppPos)

   #Simulate my step
   myPos,myPts = calculateMaxPoints(player, myBoard)
   totalMyPts += myPts
   flipBoard(player, myBoard, myPos)

   #Simulate opponent step
   oppPos,oppPts = calculateMaxPoints(opponent, myBoard)
   totalOppPts += oppPts
   flipBoard(opponent, myBoard, oppPos)

   return (totalMyPts - totalOppPts)


def flipBoard(player, board, pos):
   opponent = 'B' if player == 'W' else 'W'
   adjacent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

   board[pos[0]] = board[pos[0]][0:pos[1]] + player + board[pos[0]][pos[1]+1:]

   for adj in adjacent:
      x = pos[0]+adj[0]
      y = pos[1]+adj[1]
      curPos = (x,y)
      if x >= 0 and x < 8 and y >= 0 and y < 8:
		   if board[x][y] == opponent:
			   points = countPoints(player, board, curPos, adj, 1)
			   if points > 0:
				   flip(player,board,curPos,adj)


def flip(player, board, pos, adj):
   opponent = 'B' if player == 'W' else 'W'

   if board[pos[0]][pos[1]] == player:
	   return
   elif board[pos[0]][pos[1]] == opponent:
	   board[pos[0]] = board[pos[0]][0:pos[1]] + player + board[pos[0]][pos[1]+1:]

   x = pos[0]+adj[0]
   y = pos[1]+adj[1]
   curPos = (x,y)

   flip(player, board, curPos, adj)


def calculateMaxPoints(player,board):
   pos = (-1,-1)
   maxPoints = 0

   for i in range(0,len(board)):
      for j in range(0, len(board[i])):
         if board[i][j] == '-':
            points = checkMove(player, board, (i,j))

            if points > 0:
                  if points > maxPoints or pos==(-1,-1):
                     pos = (i,j)
                     maxPoints = points

   return pos, maxPoints

# Count total points for this move
def checkMove(player, board, pos):
   opponent = 'B' if player == 'W' else 'W'
   adjacent = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
   points = 0

   for adj in adjacent:
		x = pos[0]+adj[0]
		y = pos[1]+adj[1]
		curPos = (x,y)
		if x >= 0 and x < 8 and y >= 0 and y < 8:
			if  board[x][y] == opponent:
				points += countPoints(player, board, curPos, adj, 1)

   return points


# Count points in one direction
def countPoints(player, board, pos, direction, accumPts): 
   corners = [(0,0),(0,7),(7,0),(7,7)]
   corner_edges = [(1,0),(1,1),(0,1),(6,0),(6,1),(7,1),(0,6),(1,6),(1,7),(7,6),(6,6),(6,7)]
   edges = []

   for i in range(1,7):
      edges.append((0,i))
      edges.append((i,0))
      edges.append((7,i))
      edges.append((i,7))
        
   opponent = 'B' if player == 'W' else 'W'
   x = pos[0]+direction[0]
   y = pos[1]+direction[1]
   curPos = (x,y)

   if x < 0 or x > 7 or y < 0 or y > 7:
      return 0
   if board[x][y] == '-':
      return 0
   if board[x][y] == player:
      return accumPts
   elif board[x][y] == opponent:
        pts = 2 
        if (x,y) in corners:
            pts = 10 
        elif (x,y) in edges:
            pts = 4 
        elif (x,y) in corner_edges:
            pts = 1 
        return countPoints(player, board, curPos, direction, accumPts+pts)

# Head ends here

def nextMove(player,board):
   maxPoints = 0
   pos = (-1,-1)

   edges = []

   for i in range(1,7):
      edges.append((0,i))
      edges.append((i,0))
      edges.append((7,i))
      edges.append((i,7))

   for i in range(0,len(board)):
      for j in range(0, len(board[i])):
         if board[i][j] == '-':
            points = checkMove(player, board, (i,j))
            if points > 0:
               points = simulateMove(player, board, (i,j), points)

	       print "Points for pos (%i,%i) = %i" % (i,j,points)
               if points > maxPoints or pos == (-1,-1):
                  maxPoints = points
                  pos = (i,j)

   return pos[0],pos[1]

#TAIL HERE            
            
player = raw_input()

board = []
for i in xrange(0, 8):
    board.append(raw_input())

a,b = nextMove(player,board)
print a,b

