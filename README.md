# 2D Maze Game
Toy project I created as apart of a mini "capture the flag" type
competition.

## Running server locally
1. Create Python virtual environment (optional)
```
% python3 -m venv <venv name>
% source <venv name>/bin/activate
```

2. Install requirements
```
% pip -r requirements
```

3. Run the maze server
```
# Starts the flask server on port 8080
% FLASK_APP=server python -m flask run -p 8080
```

### Running simulation with fake client
Run a client that randomly sends directional movements to the server.
```
% python simulate_gameplay.py
```

### Running simulation without server-client architecture
Runs a game simulation with server component.
```
% python simulate_gameplay
```

## Endpoints
API is extremely minimal. Examples below:

### Create a game
Creates and returns game information. Note that session attribute will
be used in subsequent requests to the endpoints documented below.
```
(venv) ~/workspaces/escape
% curl 34.214.234.63:80/game
{"game_state":"STARTED","player_position":{"col":0,"row":9},"session":"1cd62512-e195-4651-bd9e-ee2319bde682","winning_position":{"col":9,"row":0}}
```

### Get game state
Returns game information.
```
(venv) ~/workspaces/escape
% curl 34.214.234.63:80/game/1cd62512-e195-4651-bd9e-ee2319bde682
{"game_state":"STARTED","player_position":{"col":0,"row":9},"session":"1cd62512-e195-4651-bd9e-ee2319bde682","winning_position":{"col":9,"row":0}}
```

### Send direction

URL parameter `direction` can be used to send directional movements to
the server. Response returns game information. Note that if a movement
fails (e.g., you hit a wall) the only indication is comparing player
position before/after the request (if position has not changed, the
player has hit a wall).
```
(venv) ~/workspaces/escape
% curl 34.214.234.63:80/game/1cd62512-e195-4651-bd9e-ee2319bde682\?direction=UP
{"game_state":"STARTED","player_position":{"col":0,"row":8},"session":"1cd62512-e195-4651-bd9e-ee2319bde682","winning_position":{"col":9,"row":0}}
```

# 2D Maze Generation
This repo contains `mazy.py`, which implements a graph-based 2D map
generation that makes the following guarantees:
* Every space on the map is reachable (no "dead spaces")
* Only one correct path (no cyclical paths)

![Maze Generation](./README/maze_generation.gif)
