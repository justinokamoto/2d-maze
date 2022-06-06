import argparse
import logging
import random
import requests

from board import Direction
from game import Game, GameState


def simulate_random(turns):
    game = Game()

    for i in range(turns):
        directions = Direction.options()
        direction = Direction(directions[random.randint(0, len(directions) - 1)])
        game.take_turn(direction)
        if game.state == GameState.ENDED:
            logging.info(f"Game has ended in {game.turn_counter} turns.")
            break


def simulate_random_client(turns, host, port):
    session = requests.get(f"http://{host}:{port}/game").json().get("session")

    for i in range(turns):
        directions = Direction.options()
        direction = Direction(directions[random.randint(0, len(directions) - 1)])
        game_json = requests.get(f"http://{host}:{port}/game/{session}?direction={direction.value}").json()
        logging.info(game_json)
        if "error" in game_json:
            raise Exception(game_json["error"])
        elif game_json["game_state"] == GameState.ENDED.value:
            logging.info(f"Game has ended.")
            break


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Simulate gameplay.")
    parser.add_argument("--num-turns", type=int, default=10000)
    parser.add_argument("--no-server", action="store_true")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)

    args = parser.parse_args()

    if args.no_server:
        logging.getLogger().setLevel(logging.DEBUG)
        simulate_random(args.num_turns)
    else:
        simulate_random_client(args.num_turns, args.host, args.port)
