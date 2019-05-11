from bearlibterminal import terminal as blt
import tcod

from const import Layers
from game_states import GameStates


def kill_player(player):
    player.char = "%"
    player.color = "red"

    return "You died!", GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = f"{monster.name.capitalize()} is dead!"

    monster.char = "%"
    monster.color = "red"
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f"remains of {monster}"
    monster.layer = Layers.ITEMS

    return death_message
