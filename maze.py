from typing import Tuple, List
import random
from weakref import WeakSet

# TODO: Make simple callable
# TODO: Standardize on row,col opposed to x,y
# TODO: 'traversable' edges are really implied by 'blocked' and vice-versa, right? (we can remove one)


class MazeNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        # Edges are weakrefs as they do should not affect lifecycle of
        # `MazeNode` objects or confuse GC w/ circular refs
        self.traversable = WeakSet()
        self.blocked = WeakSet()
        # 'visited' here denotes whether node has been visited when
        # building out the map
        self.visited = False

    @staticmethod
    def add_traversable_edge(n1, n2):
        n1.traversable.add(n2)
        n2.traversable.add(n1)

    @staticmethod
    def add_blocked_edge(n1, n2):
        n1.blocked.add(n2)
        n2.blocked.add(n1)

    @staticmethod
    def remove_traversable_edge(n1, n2):
        n1.traversable.remove(n2)
        n2.traversable.remove(n1)

    @staticmethod
    def remove_blocked_edge(n1, n2):
        n1.blocked.remove(n2)
        n2.blocked.remove(n1)


# TODO: Rename these classes to [Maze|Board]Generator and make them callables
class Maze:
    def __init__(self, cols=10, rows=10):
        # NOTE: Values could be derived from board shape?
        self.cols = cols
        self.rows = rows
        # Instantiate board
        self.board = [[ MazeNode(row, col) for col in range(cols) ] for row in range(rows)]

    def get_node(self, x, y):
        """convenience that does bound checking"""
        if x < 0 or x > self.rows - 1 or \
           y < 0 or y > self.cols - 1:
            return None
        return self.board[x][y]

    def get_neighbors(self, x, y, filter_blocked=False) -> Tuple[List[MazeNode], List[Tuple[int, int]]]:
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
        if any neighbors are reachable (recursive)
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

    def build(self, row=0, col=0):
        node = self.get_node(row, col)
        node.visited = True
        neighbors = self.get_neighbors(node.row, node.col)
        for n in neighbors:
            if n.visited:
                continue
            # Add blocked edge, and determine if it created 'island'
            MazeNode.add_blocked_edge(n, node)

            if self.is_reachable(n.row, n.col):
                # If node is not isolated, optionally keep blocked edge
                if random.randint(0,1):
                    continue
            # Replace blocked edge w/ traversable edge
            MazeNode.remove_blocked_edge(n, node)
            MazeNode.add_traversable_edge(n, node)

            self.build(n.row, n.col)
