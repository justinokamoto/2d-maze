import logging
import random

from board import Direction
from game import Game, GameState


def simulate_random(turns=10000):
    game = Game()

    for i in range(turns):
        directions = Direction.options()
        direction = Direction(directions[random.randint(0, len(directions) - 1)])
        game.take_turn(direction)
        if game.state == GameState.ENDED:
            logging.info(f"Game has ended in {game.turn_counter} turns.")
            break


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    simulate_random()
