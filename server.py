from flask import Flask
from flask_restful import reqparse

from game import Game, GameState
from board import Direction

from typing import Dict
import logging
import uuid


app = Flask("EscapeServer")
sessions_to_games: Dict[str,Game] = {}


@app.route("/")
def index():
    return "Nothing to see here."

@app.route("/game")
def game_create():
    game = Game()
    session = str(uuid.uuid5())
    sessions_to_games[session] = game
    return {
        "pos": game.current_turn().pos,
        "game_state": game.state
    }

@app.route("/game/<session>")
def game_update(session):
    game = sessions_to_games.get(session)
    if game is None:
        return {
            "error": "Game with session {session} not found."
        }

    parser = reqparse.RequestParser()
    parser.add_argument('direction',
                        required=True,
                        type=str,
                        choices=Direction.options(),
                        help="Move must be one of {', '.join(Direction.options())}!")
    parser.parse_args()
    game.take_turn(parser.direction)
    return {
        "pos": game.current_turn().pos,
        "game_state": game.state
    }

@app.route("/game/<session>")
def game_get(session):
    game = sessions_to_games.get(session)
    if game is None:
        return {
            "error": "Game with session {session} not found."
        }
    if game.state == GameState.ENDED:
        logging.info(f"Session {session} won.")
    return {
        "pos": game.current_turn().pos,
        "game_state": game.state
    }
