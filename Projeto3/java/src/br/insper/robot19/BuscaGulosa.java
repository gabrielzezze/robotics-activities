package br.insper.robot19;

import java.awt.geom.Path2D;
import java.util.Comparator;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

public class BuscaGulosa {

    private Block start = null;
    private Block end = null;
    private GridMap map = null;
    private boolean[][] visited;

    private LinkedList<Node> border;

    public BuscaGulosa(GridMap map, Block start, Block end) {
        this.map = map;
        this.start = start;
        this.end = end;
        visited = new boolean[map.getHeight()][map.getWidth()];

        for (int i=0; i<map.getHeight(); i++){
            for (int j=0; j<map.getWidth(); j++){
                visited[i][j] = false;
            }
        }
    }

    public Node buscar() {

        Node root = new Node(start, null, null, 0);

        //Limpa a fronteira e insere o nó raiz
        border = new LinkedList<Node>();
        border.add(root);

        while(!border.isEmpty()) {

            Node node = border.remove();
            Block atual = node.getValue();

            visited[atual.row][atual.col] = true;

            if(atual.row == end.row && atual.col == end.col) {
                return node;

            } else{


                for(RobotAction acao : RobotAction.values()) {

                    Block proximo = map.nextBlock(atual, acao);

                    if (proximo != null && proximo.type != BlockType.WALL && !visited[proximo.row][proximo.col]) {
                        Node novoNode = new Node(proximo, node, acao, proximo.type.cost);
                        border.add(novoNode);
                    }
                }

                border.sort(new Comparator<Node>() {
                    @Override
                    public int compare(Node o1, Node o2) {
                        if(o1.getValue().getHeuristica(end.row, end.col) > o2.getValue().getHeuristica(end.row, end.col)){
                            return 1;
                        }
                        else if(o1.getValue().getHeuristica(end.row, end.col) < o2.getValue().getHeuristica(end.row, end.col)){
                            return -1;
                        }
                        else{
                            return 0;
                        }
                    }
                });

            }
        }
        return null;
    }

    /**
     * Resolve o problema com base em busca, realizando
     * o backtracking após chegar ao estado final
     *
     * @return A solução encontrada
     */
    public RobotAction[] resolver() {

        // Encontra a solução através da busca
        Node destino = buscar();
        if(destino == null) {
            return null;
        }

        //Faz o backtracking para recuperar o caminho percorrido
        Node atual = destino;
        Deque<RobotAction> caminho = new LinkedList<RobotAction>();
        while(atual.getAction() != null) {
            caminho.addFirst(atual.getAction());
            atual = atual.getParent();
        }
        return caminho.toArray(new RobotAction[caminho.size()]);
    }
}

