# 2D Maze Game
This is a simple 2D maze game I created for a mini "capture the flag"
type game.

TODO: Description. Document endpoints.

## Running locally
Install requirements:
```
pip -r requirements
```
### Running server
Run the maze server.
```
# Starts the flask server on port 8080
FLASK_APP=server python -m flask run -p 8080
```
### Running simulated client
Run a client that randomly sends directional movements to the server.
```
python simulate_gameplay.py
```

# 2D Maze Generation
This repo contains `mazy.py`, which implements a graph-based 2D map
generation that makes the following guarantees:
* Every space on the map is reachable (no "dead spaces")
* Only one correct path (no cyclical paths)

![Maze Generation](./README/maze_generation.gif)
