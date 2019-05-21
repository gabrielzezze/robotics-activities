package br.insper.robot19;

public class Block {
	
	public final int row;
	public final int col;
	private boolean visited;
	public final BlockType type;
	
	public Block(int i, int j, BlockType type) {
		this.row = i;
		this.col = j;
		this.type = type;
		this.visited = false;
	}


	public int getHeuristica(int endRow, int endCol){
		return Math.abs(row-endRow) + Math.abs(col-endCol);
	}

	public void setVisited(boolean visited) {
		this.visited = visited;
	}

	public boolean isVisited() {
		return visited;
	}
}
