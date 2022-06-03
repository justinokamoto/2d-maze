from enum import Enum

from board import Board, Direction
from maze import Maze
import logging
from player import Player

logger = logging.getLogger()


class GameState(Enum):
    STARTED = "STARTED"
    ENDED = "ENDED"


class Game:
    def __init__(self):
        maze = Maze()
        maze.build() # TODO: Have this return board or be callable

        self._board = Board(maze.board)
        self._players = [ Player("player1", self._board.start_pos) ]
        self.turn_counter = 0
        self.state = GameState.STARTED

    def is_valid(self):
        return len(self._players) > 0

    def has_winner(self):
        return next(filter(lambda p: p.pos == self._board.end_pos for p in self._players), None) is not None

    def current_turn(self) -> Player:
        return self._players[self.turn_counter % len(self._players)]

    def take_turn(self, direction):
        if self.state == GameState.ENDED:
            logger.error("Game has ended.")
            return

        player = self.current_turn()
        des_pos = Direction.translation(player.pos, direction)

        logger.debug(f"Player {player.name} attempts to move {player.pos} -> {des_pos}")

        if not self._board.can_move(player.pos, des_pos):
            logger.debug(f"Player {player.name} turn failed.")
            return

        # Update state
        player.pos = des_pos # Update player position
        self.turn_counter += 1 # Update turn counter
        if player.pos == self._board.end_pos: # Update state (if winner)
            logger.debug(f"Player {player.name} won.")
            self.state = GameState.ENDED
