import logging
import os

import networkx as nx
import matplotlib.pyplot as plt

from maze import Maze


class VisualMaze(Maze):
    def __init__(self, row, col):
        # Track num frames created
        self.frame_count = 0
        super().__init__(row, col)

    def build(self, row=0, col=0):
        super().build(row, col)
        self.visualize()

    def visualize(self):
        def create_node_label(node):
            # Derives node label from position
            return f"N{node.row},{node.col}"
        # TODO: draws duplicate edges...We should filter out half
        G = nx.Graph()
        visited_node_pos = {}
        unvisited_node_pos = {}
        traversable_edges = []
        blocked_edges = []
        for row in range(self.rows):
            for col in range(self.cols):
                node = self.board[row][col]
                node_label = create_node_label(node)
                if node.visited:
                    visited_node_pos[node_label] = (row, col)
                else:
                    unvisited_node_pos[node_label] = (row, col)
                for n in node.traversable:
                    traversable_edges.append((node_label, create_node_label(n)))
                for n in node.blocked:
                    blocked_edges.append((node_label, create_node_label(n)))

        all_node_pos = visited_node_pos.copy()
        all_node_pos.update(unvisited_node_pos)

        # G.add_edges_from(edges) Don't worry about building a graph...Just build enough for visualization
        G.add_nodes_from(visited_node_pos.keys())
        G.add_nodes_from(unvisited_node_pos.keys())

        nx.draw_networkx_nodes(G, visited_node_pos, node_size=10, nodelist=visited_node_pos.keys(), node_color='green') # Make sure to draw all nodes
        nx.draw_networkx_nodes(G, unvisited_node_pos, node_size=10, nodelist=unvisited_node_pos.keys(), node_color='black') # Make sure to draw all nodes

        nx.draw_networkx_edges(G, all_node_pos, edgelist=traversable_edges, edge_color='black', arrows=False)
        nx.draw_networkx_edges(G, all_node_pos, edgelist=blocked_edges, edge_color='red', arrows=False)

        plt.savefig(os.path.join("build", f"frame_{self.frame_count}.png"))
        plt.show()

        self.frame_count += 1
