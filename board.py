from collections import namedtuple
from enum import Enum


PositionTuple = namedtuple('PositionTuple', 'row col')

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @staticmethod
    def translation(pos, direction) -> PositionTuple:
        if direction == Direction.LEFT:
            return PositionTuple(pos.row, pos.col - 1)
        elif direction == Direction.RIGHT:
            return PositionTuple(pos.row, pos.col + 1)
        elif direction == Direction.UP:
            return PositionTuple(pos.row - 1, pos.col)
        elif direction == Direction.DOWN:
            return PositionTuple(pos.row + 1, pos.col)
        else:
            raise TypeError("direction parameter must be of type Direction")

    # TODO: Cache result
    @staticmethod
    def options():
        return [x.value for x in Direction]


class Board:
    def __init__(self, board):
        # 2D array of MazeNode objects
        self.board = board
        # Using list (not numpy.ndarray) so we'll cache dimensions for
        # clarity
        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0])
        # TODO: private w/ getter
        # Defaults to bot left
        self.start_pos = PositionTuple(self.num_rows - 1, 0)
        # TODO: private w/ getter
        # Defaults to top right
        self.end_pos = PositionTuple(0, self.num_cols - 1)

    def can_move(self, cur_pos, des_pos) -> bool:
        if des_pos.row >= 0 and des_pos.row < self.num_rows and \
           des_pos.col >= 0 and des_pos.col < self.num_cols:
            cur_node = self.board[cur_pos.row][cur_pos.col]
            des_node = self.board[des_pos.row][des_pos.col]
            if des_node in cur_node.traversable:
                self.pos = PositionTuple(des_node.row, des_node.col)
                return True
        return False
