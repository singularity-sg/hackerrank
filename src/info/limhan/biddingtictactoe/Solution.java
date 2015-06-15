package info.limhan.biddingtictactoe;

import java.util.Scanner;

public class Solution {
	
	public static final int[] NORTH = new int[] { -1, 0 };
	public static final int[] NORTHEAST = new int[] { -1, 1 };
	public static final int[] EAST = new int[] { 0, 1 };
	public static final int[] SOUTHEAST = new int[] { 1, 1 };
	public static final int[] SOUTH = new int[] { 1, 0 };
	public static final int[] SOUTHWEST = new int[] { 1, -1};
	public static final int[] WEST = new int[] { 0, -1};
	public static final int[] NORTHWEST = new int[] { -1, -1 };
	
	char player;
	String typeOfMove;
	int[][] bids;
	char[][] board;
	
	public Solution(char player, String typeOfMove, int[][] bids, char[][] board) {
		this.player = player;
		this.typeOfMove = typeOfMove;
		this.bids = bids;
		this.board = board;
	}

    public static void main(String[] args) {
    	
    	char player = ' ';
    	String typeOfMove = null;
    	int[][] bids = new int[2][];
    	char[][] board = new char[3][3];
    	
        try(Scanner scanner = new Scanner(System.in)) {
        	
        	int lineNum = 0;
        	while(scanner.hasNextLine()) {
        		String line = scanner.nextLine();
        		String[] tokens;
        		if(lineNum >= 0 && lineNum <= 6) {
	        		switch(lineNum) {
	        			case 0 : player = line.length() > 0 ? line.charAt(0) : 'X'; break;
	        			case 1 : typeOfMove = line.trim(); break;
	        			case 2 : tokens = line.split(" ");
	        					 bids[0] = new int[tokens.length];
	        					 for(int i=0;i<tokens.length;i++) {
	        						 if(!tokens[i].trim().isEmpty()) {
	        							 bids[0][i] = Integer.parseInt(tokens[i].trim());
	        						 }
	        					 }
	        					 break;
	        			case 3 : tokens = line.split(" ");
	        					 bids[1] = new int[tokens.length];
								 for(int i=0;i<tokens.length;i++) {
									 if(!tokens[i].trim().isEmpty()) {
										 bids[1][i] = Integer.parseInt(tokens[i].trim());
									 }
								 }
								 break;
	        			case 4 :
	        			case 5 :
	        			case 6 :
	        					 board[lineNum-4][0] = line.trim().charAt(0);
						 		 board[lineNum-4][1] = line.trim().charAt(1);
						 		 board[lineNum-4][2] = line.trim().charAt(2);
						 		 break;
	        		}
        		}
        		lineNum++;
        	}
        }
        
        Solution solution = new Solution(player, typeOfMove, bids, board);
        solution.makeMove();
    }

    
    /** 
     * Make your move in this method. There should already by the following field variables available
     * String player
     * String typeOfMove : BID | MOVE
     * int[2][] bids
     * char[3][3] board
     */
	protected void makeMove() {
		if(isPlay()) {
			int[] move = findMove(this.player, this.board);
			System.out.println(String.format("%d %d", move[0], move[1]));
		}
		if(isBid()) {
			System.out.println(currentBidsAvailable(this.player, this.bids) / 2);
		}
	}
	
	private boolean isBid() {
		if("BID".equalsIgnoreCase(typeOfMove)) {
			return true;
		}
		return false;
	}
	
	private boolean isPlay() {
		if("PLAY".equalsIgnoreCase(typeOfMove)) {
			return true;
		}
		return false;
	}
	
	protected int currentBidsAvailable(char player, int[][] bids) {
		int bidsLeft = 4;
		
		if('X' == player || 'x' == player) {
			for(int i=0;i<bids[0].length;i++) {
				if(bids[0][i] > bids[1][i]) {
					bidsLeft -= bids[0][i];
				} 
				if(bids[0][i] < bids[1][i]) {
					bidsLeft += bids[1][i]; 
				}
			}
		}
		if('O' == player || 'o' == player) {
			for(int i=0;i<bids[1].length;i++) {
				if(bids[1][i] > bids[0][i]) {
					bidsLeft -= bids[1][i];
				} 
				if(bids[1][i] < bids[0][i]) {
					bidsLeft += bids[0][i]; 
				}
			}

		}
		
		return bidsLeft;
	}
	
	protected int[] findMove(char player, char[][] board) {
		
		int maxPoints = 0;
		int[] maxPointsPos = new int[] {0,0};
		
		for(int i=0;i<board.length;i++) {
			for(int j=0;j<board[i].length;j++) {
				if(board[i][j] == '_'){
					int[] currPos = new int[]{i,j};
					char opponent = player == 'X' || player == 'x' ? 'O' : 'X';
					
					int points = evaluateOpenOptions(player, board, currPos);
					points += evaluateWins(player, board, currPos);
					points += evaluateOpponent(opponent, board, currPos);
					
					if(points > maxPoints) {
						maxPoints = points;
						maxPointsPos = currPos;
					}
				}
			}
		}
		
		return maxPointsPos;
	}

	protected int evaluateOpponent(char opponent, char[][] board, int[] currPos) {
		int count = 0;
		int points = 0;
		boolean onlyMoves = true;
		
		count = 1 + scanDirection(opponent, board, currPos, SOUTH, onlyMoves) + scanDirection(opponent, board, currPos, NORTH, onlyMoves);
		if(count == board.length) {
			points+=2;
		}
		count = 1 + scanDirection(opponent, board, currPos, EAST, onlyMoves) + scanDirection(opponent, board, currPos, WEST, onlyMoves);
		if(count == board.length) {
			points+=2;
		}
		count = 1 + scanDirection(opponent, board, currPos, NORTHEAST, onlyMoves) + scanDirection(opponent, board, currPos, SOUTHWEST, onlyMoves);
		if(count == board.length) {
			points+=2;
		}
		count = 1 + scanDirection(opponent, board, currPos, NORTHWEST, onlyMoves) + scanDirection(opponent, board, currPos, SOUTHEAST, onlyMoves);
		if(count == board.length) {
			points+=2;
		}
		
		return points;
	}
	
	protected int evaluateOpenOptions(char player, char[][] board, int[] currPos) {
		int count = 0;
		int points = 0;
		boolean onlyMoves = false;
		
		count = 1 + scanDirection(player, board, currPos, SOUTH, onlyMoves) + scanDirection(player, board, currPos, NORTH, onlyMoves);
		if(count == board.length) {
			points++;
		}
		count = 1 + scanDirection(player, board, currPos, EAST, onlyMoves) + scanDirection(player, board, currPos, WEST, onlyMoves);
		if(count == board.length) {
			points++;
		}
		count = 1 + scanDirection(player, board, currPos, NORTHEAST, onlyMoves) + scanDirection(player, board, currPos, SOUTHWEST, onlyMoves);
		if(count == board.length) {
			points++;
		}
		count = 1 + scanDirection(player, board, currPos, NORTHWEST, onlyMoves) + scanDirection(player, board, currPos, SOUTHEAST, onlyMoves);
		if(count == board.length) {
			points++;
		}
		
		return points;
	}
	
	protected int evaluateWins(char player, char[][] board, int[] currPos) {
		int count = 0;
		int points = 0;
		boolean onlyMoves = true;
		
		count = 1 + scanDirection(player, board, currPos, SOUTH, onlyMoves) + scanDirection(player, board, currPos, NORTH, onlyMoves);
		if(count == board.length) {
			points+=3;
		}
		count = 1 + scanDirection(player, board, currPos, EAST, onlyMoves) + scanDirection(player, board, currPos, WEST, onlyMoves);
		if(count == board.length) {
			points+=3;
		}
		count = 1 + scanDirection(player, board, currPos, NORTHEAST, onlyMoves) + scanDirection(player, board, currPos, SOUTHWEST, onlyMoves);
		if(count == board.length) {
			points+=3;
		}
		count = 1 + scanDirection(player, board, currPos, NORTHWEST, onlyMoves) + scanDirection(player, board, currPos, SOUTHEAST, onlyMoves);
		if(count == board.length) {
			points+=3;
		}
		
		return points;
	}

	protected int scanDirection(char player, char[][] board, int[] currPos, int[] dirVec, boolean playerOnly) {
		int[] newPos = new int[] { currPos[0] + dirVec[0], currPos[1] + dirVec[1] };
		
		if(newPos[0] >= board.length || newPos[0] < 0 || newPos[1] >= board.length || newPos[1] < 0) {
			return 0;
		}
		
		if(playerOnly) {
			if(board[newPos[0]][newPos[1]] == player) {
				return 1 + scanDirection(player, board, newPos, dirVec, playerOnly);
			} else {
				return 0;
			}
		} else {
			if(board[newPos[0]][newPos[1]] == '_' || board[newPos[0]][newPos[1]] == player) {
				return 1 + scanDirection(player, board, newPos, dirVec, playerOnly);
			} else {
				return 0;
			}
		}
	}
}