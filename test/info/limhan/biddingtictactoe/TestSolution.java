package info.limhan.biddingtictactoe;

import static org.assertj.core.api.Assertions.*;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.junit.Test;
import org.mockito.Mockito;

public class TestSolution {

	Solution unit;
	
	@Test
	public void testParsingSystemInput() throws Exception {
		byte[] buffer = new byte[32];
		InputStream is = new ByteArrayInputStream(buffer);
		InputStream spyIs = Mockito.spy(is);
		System.setIn(spyIs);
		
		String inString = "X\nBID\n1 2\n2 1\n__O\n_X_\n___\n";
		
		ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
		executor.schedule(() -> {
			System.arraycopy(inString.getBytes(), 0, buffer, 0, inString.getBytes().length);
		}, 200, TimeUnit.MILLISECONDS);
		
		Solution.main(new String[]{});
		
		Mockito.verify(spyIs, Mockito.atLeastOnce()).read(Mockito.any(byte[].class), Mockito.anyInt(), Mockito.anyInt());
	}
	
	@Test
	public void testParsingFirstInput() throws Exception {
		byte[] buffer = new byte[32];
		InputStream is = new ByteArrayInputStream(buffer);
		InputStream spyIs = Mockito.spy(is);
		System.setIn(spyIs);
		
		String inString = "X\nBID\n\n\n___\n___\n___\n";
		
		ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
		executor.schedule(() -> {
			System.arraycopy(inString.getBytes(), 0, buffer, 0, inString.getBytes().length);
		}, 200, TimeUnit.MILLISECONDS);
		
		Solution.main(new String[]{});
		
		Mockito.verify(spyIs, Mockito.atLeastOnce()).read(Mockito.any(byte[].class), Mockito.anyInt(), Mockito.anyInt());
	}
	
	@Test
	public void testFindMove() throws Exception {
		
		try (PrintStream spyPs = Mockito.spy(System.out); PrintStream original = System.out) {
			System.setOut(spyPs);
			
			Solution solution = createSolution();
			
			int[] move = solution.findMove('X', solution.board);
			
			assertThat(move).isEqualTo(new int[] { 1,1 });
			
			System.setOut(original);
		}
		
	}
	
	@Test
	public void testFindMove2() throws Exception {
		
		try (PrintStream spyPs = Mockito.spy(System.out); PrintStream original = System.out) {
			System.setOut(spyPs);
			
			Solution solution = createSolution();
			
			
			char[] rowOne   = new char[] { 'O','_','_' };
			char[] rowTwo   = new char[] { '_','X','_' };
			char[] rowThree = new char[] { 'O','_','_' };
			char[][] board = new char[][] { rowOne, rowTwo, rowThree };
			
			int[] move = solution.findMove('X', board);
			
			assertThat(move).isEqualTo(new int[] { 1,0 });
			
			System.setOut(original);
		}
		
	}
	
	@Test
	public void testFindMove3() throws Exception {
		
		try (PrintStream spyPs = Mockito.spy(System.out); PrintStream original = System.out) {
			System.setOut(spyPs);
			
			Solution solution = createSolution();
			
			
			char[] rowOne   = new char[] { '0','_','_' };
			char[] rowTwo   = new char[] { '_','_','_' };
			char[] rowThree = new char[] { 'X','_','0' };
			char[][] board = new char[][] { rowOne, rowTwo, rowThree };
			
			int[] move = solution.findMove('X', board);
			
			assertThat(move).isEqualTo(new int[] { 1,1 });
			
			System.setOut(original);
		}
		
	}
	
	@Test
	public void testFindMove4() throws Exception {
		
		try (PrintStream spyPs = Mockito.spy(System.out); PrintStream original = System.out) {
			System.setOut(spyPs);
			
			Solution solution = createSolution();
			
			
			char[] rowOne   = new char[] { '0','_','X' };
			char[] rowTwo   = new char[] { '_','_','_' };
			char[] rowThree = new char[] { '0','_','X' };
			char[][] board = new char[][] { rowOne, rowTwo, rowThree };
			
			int[] move = solution.findMove('X', board);
			
			assertThat(move).isEqualTo(new int[] { 1,2 });
			
			System.setOut(original);
		}
		
	}
	
	@Test
	public void testMakeMove() throws Exception {
		try (PrintStream spyPs = Mockito.spy(System.out); PrintStream original = System.out) {
			System.setOut(spyPs);
			
			Solution solution = createSolution();
			
			solution.makeMove();
			
			Mockito.verify(spyPs, Mockito.times(1)).println("1 1");
			
			System.setOut(original);
		}
	}
	
	@Test
	public void testBidsLeft() throws Exception {
		Solution solution = createSolution();
		
		int[][] bids = new int[2][];
		bids[0] = new int[] { 2, 0, 1 };
		bids[1] = new int[] { 1, 2, 2 }; 
		
		assertThat(solution.currentBidsAvailable('X', bids)).isEqualTo(6);
		assertThat(solution.currentBidsAvailable('O', bids)).isEqualTo(2);
		
		bids = new int[2][];
		bids[0] = new int[] { 4, 0, 1 };
		bids[1] = new int[] { 1, 1, 2 }; 
		
		assertThat(solution.currentBidsAvailable('X', bids)).isEqualTo(3);
		assertThat(solution.currentBidsAvailable('O', bids)).isEqualTo(5);
	}
	
	private Solution createSolution() {
		int[][] bids = new int[2][2];
		char[][] board = new char[3][3];
		
		for(int i=0;i<board.length;i++) {
			Arrays.fill(board[i], '_');
		}
		
		Solution solution = new Solution('X', "PLAY", bids, board);
		return solution;
	}
}
