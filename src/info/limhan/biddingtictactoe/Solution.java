package info.limhan.biddingtictactoe;

import java.util.Scanner;

public class Solution {
	
	String player;
	String typeOfMove;
	int[][] bids;
	char[][] board;
	
	public Solution(String player, String typeOfMove, int[][] bids, char[][] board) {
		this.player = player;
		this.typeOfMove = typeOfMove;
		this.bids = bids;
		this.board = board;
	}

    public static void main(String[] args) {
    	
    	String player = null;
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
	        			case 0 : player = line.trim(); break;
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
			int[] move = findMove(this.board);
			System.out.println(String.format("%d %d", move[0], move[1]));
		}
		if(isBid()) {
			System.out.println(currentBidsAvailable(this.bids) / 2);
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
	
	protected int currentBidsAvailable(int[][] bids) {
		int bidsLeft = 4;
		
		if("X".equalsIgnoreCase(this.player)) {
			for(int i=0;i<bids[0].length;i++) {
				if(bids[0][i] > bids[1][i]) {
					bidsLeft -= bids[0][i];
				} 
				if(bids[0][i] < bids[1][i]) {
					bidsLeft += bids[1][i]; 
				}
			}
		}
		if("O".equalsIgnoreCase(this.player)) {
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
	
	protected int[] findMove(char[][] board) {
		
		for(int i=0;i<board.length;i++) {
			for(int j=0;j<board[i].length;j++) {
				if(board[i][j] == '_') {
					return new int[] { i, j };
				}
			}
		}
		
		return new int[] {-1,-1};
	}
}