package br.insper.robot19;

public enum BlockStatus {

	START('0'),
	GOAL('G'),
	ROUTE('o');
	
	public final char symbol;
	private BlockStatus(char symbol) {
		this.symbol = symbol;
	}

}
