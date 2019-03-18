from enum import Enum, auto


class GameStates(Enum):
    INITIALIZE = 0
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    EXIT = 999
