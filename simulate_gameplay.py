import logging
import random
import requests

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


def simulate_random_client(turns=10000, ip="127.0.0.1", port=8080):
    session = requests.get(f"http://{ip}:{port}/game").json().get("session")

    for i in range(turns):
        directions = Direction.options()
        direction = Direction(directions[random.randint(0, len(directions) - 1)])
        game_json = requests.get(f"http://{ip}:{port}/game/{session}?direction={direction.value}").json()
        logging.info(game_json)
        if "error" in game_json:
            raise Exception(game_json["error"])
        elif game_json["game_state"] == GameState.ENDED.value:
            logging.info(f"Game has ended.")
            break


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    # TODO: Add option for local or remote simulation!

    simulate_random_client()
