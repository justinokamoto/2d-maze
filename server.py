from flask import Flask, request
from flask_restful import reqparse
from flask.logging import default_handler

from game import Game, GameState
from board import Direction

from typing import Dict
import logging
import uuid


logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(default_handler)

app = Flask("EscapeServer")
sessions_to_games: Dict[str,Game] = {}


# TODO: Smarter serialization
def response(game, session):
    return {
        "session": session,
        "player_position": {
            "row": game.current_turn().pos.row,
            "col": game.current_turn().pos.col
        },
        "winning_position": {
            "row": game._board.end_pos.row,
            "col": game._board.end_pos.col
        },
        "game_state" : game.state.value
    }

@app.route("/")
def index():
    return { "error": "Nothing to see here." }

@app.route("/game")
def game_create():
    game = Game()
    session = str(uuid.uuid4())
    sessions_to_games[session] = game
    return response(game, session)

@app.route("/game/<session>")
def game_get_or_update(session):
    game = sessions_to_games.get(session)
    direction_param = request.args.get('direction')

    if game is None:
        return { "error": f"Game with session {session} not found." }
    if game.state == GameState.ENDED:
        return { "error": f"Game ended {game.turn_counter} turns." }
    if direction_param:
        try:
            direction = Direction(direction_param)
        except ValueError:
            return { "error": f"direction must be one of [{', '.join(Direction.options())}], not '{direction_param}'." }
        game.take_turn(direction)
    if game.state == GameState.ENDED:
        logging.info(f"Game with session {session} ended in {game.turn_counter} turns.")
    return response(game, session)
