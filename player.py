from board import PositionTuple

class Player:
    def __init__(self, name:str, pos:PositionTuple):
        self.name = name
        self.pos = pos
