from typing import Tuple, List
import random
import networkx as nx
import matplotlib.pyplot as plt

# TODO: Convert all x,y to row,col
# TODO: .traversable is really implied by .visited / absence of .blocked

def visualize(m):
    def create_node_label(node):
        # Derives node label from position
        return f"N{node.row},{node.col}"
    # TODO: draws multiple edges
    G = nx.Graph()
    visited_node_pos = {}
    unvisited_node_pos = {}
    traversable_edges = []
    blocked_edges = []
    for row in range(m.ROWS):
        for col in range(m.COLS):
            node = m.board[row][col]
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
    # Don't worry about building a graph...Just need for visualizing
    # G.add_edges_from(edges)
    G.add_nodes_from(visited_node_pos.keys())
    G.add_nodes_from(unvisited_node_pos.keys())

    nx.draw_networkx_nodes(G, visited_node_pos, nodelist=visited_node_pos.keys(), node_color='green') # Make sure to draw all nodes
    nx.draw_networkx_nodes(G, unvisited_node_pos, nodelist=unvisited_node_pos.keys(), node_color='black') # Make sure to draw all nodes

    nx.draw_networkx_edges(G, all_node_pos, edgelist=traversable_edges, edge_color='black', arrows=False)
    nx.draw_networkx_edges(G, all_node_pos, edgelist=blocked_edges, edge_color='red', arrows=False)

    plt.show()


class MapNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.traversable = set()
        self.blocked = set()
        self.visited = False


class Map:
    COLS, ROWS = 10, 10

    def __init__(self):
        # Instantiate board
        self.board = [[ MapNode(row, col) for col in range(self.COLS) ] for row in range(self.ROWS)]

    def get_node(self, x, y):
        """convenience that does bound checking"""
        if x < 0 or x > self.ROWS - 1 or \
           y < 0 or y > self.COLS - 1:
            return None
        return self.board[x][y]

    def get_neighbors(self, x, y, filter_blocked=False) -> Tuple[List[MapNode], List[Tuple[int, int]]]:
        # TODO: Document return type
        neighbors = filter(lambda n: n is not None, [
            self.get_node(x - 1, y),
            self.get_node(x + 1, y),
            self.get_node(x, y + 1),
            self.get_node(x, y - 1),
        ])
        if filter_blocked:
            neighbors = filter(lambda n: n not in self.get_node(x, y).blocked, neighbors)
        return list(neighbors)

    def is_reachable(self, x, y):
        """
        A node is reachable if any non-blocked neighbors are visited, or
        any neighbors are reachable (recursive)
        """
        visited_nodes = set() # TODO: Better distinguish between visited concepts
        # BFS starting from initial node
        neighbors = [self.get_node(x,y)]
        while len(neighbors) > 0:
            n = neighbors.pop()
            if n in visited_nodes:
                continue
            if n.visited:
                return True
            visited_nodes.add(n) # Add as visited
            neighbors = neighbors + self.get_neighbors(n.row, n.col, filter_blocked=True)
        return False

    def build(self, row=ROWS-1, col=0):
        """ default x,y is bottom right """
        node = self.get_node(row, col)
        node.visited = True
        neighbors = self.get_neighbors(node.row, node.col)
        for n in neighbors:
            if n.visited:
                continue
            # If node is reachable, randomly build wall or continue
            # along path
            if self.is_reachable(n.row, n.col):
                if random.randint(0,1):
                    # Edges require this circular reference! (TODO: remove this)
                    node.blocked.add(n)
                    n.blocked.add(node)
                else:
                    node.traversable.add(n)
                    n.traversable.add(node)
                    self.build(n.row, n.col)        
        visualize(self)


m = Map()
m.build()

# EIther paint boarders now OR do index checking...?


# class Board:
#     def __init__(self):
#         self.visited = np.zeros((10,10), np.uint8)
# visited = np.zeros((10,10), np.uint8)



# data structures
# is visited map
# walls (8 bit int to represent?)

# is_reachable(x,y):
# (temp visted map)
# grow

# orientations_available(x,y):
# 

# give loc [x,y] and orientation r
# mark visited
# can build wall? (is reachable?)
# if rand(.5) OR if already visited (meaning another orientation met it already)
#   build wall
# else
#   advance
#   find orientations available, and recursively call
