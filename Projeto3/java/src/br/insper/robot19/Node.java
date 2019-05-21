package br.insper.robot19;

public class Node {
	private Block value;
	private Node parent;
	private RobotAction action;
	private float pathCost;
	private boolean visited;

	public Node (Block value, Node parent, RobotAction action, float cost) {
		this.value = value;
		this.parent = parent;
		this.action = action;
		this.pathCost = parent == null ? 0 : parent.getPathCost() + cost;
		this.visited = false;
	}


	public Block getValue() {
		return value;
	}
	
	public Node getParent() {
		return parent;
	}
	
	public RobotAction getAction() {
		return action;
	}
	
	public float getPathCost() {
		return pathCost;
	}

	public boolean isVisited() {
		return visited;
	}

	public void setVisited(boolean visited) {
		this.visited = visited;
	}
}
