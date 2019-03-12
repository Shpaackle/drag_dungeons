import random
from datetime import datetime
from bearlibterminal import terminal
# from loguru import logger

from const import Tiles, MAP_SETTINGS
from camera import Camera

from entity import Entity, blocking_entities
from fov_functions import initialize_fov, update_fov
from handle_keys import handle_keys
from render_functions import render_all, clear_all
from map_objects import Dungeon, Point
from game_states import GameStates


class Game:
    def __init__(self, random_seed=None):
        if random_seed is None:
            self.random_seed = datetime.now()
        else:
            self.random_seed = random_seed

        self.dungeon = Dungeon(MAP_SETTINGS)

    def on_enter(self):
        random.seed(self.random_seed)
        self.dungeon.build_dungeon()


def main():
    game_exit = False
    random_seed = datetime.now()
    print(random_seed)
    random.seed(random_seed)
    dungeon = Dungeon(MAP_SETTINGS)
    dungeon.build_dungeon()

    game_map = dungeon.game_map

    fov_update: bool = True
    initialize_fov(game_map=game_map)

    player = Entity("Player", dungeon.starting_position, char=Tiles.PLAYER, color="white", blocks=True)
    # npc = Entity("NPC", Point(player.x + 1, player.y + 1), char="@", color="yellow")
    entities = dungeon.place_entities(player)

    camera = Camera(player)

    terminal.refresh()

    game_state = GameStates.PLAYER_TURN
    
    while not game_exit:
        key = None
        if terminal.has_input():
            key = terminal.read()

        if fov_update:
            update_fov(game_map, player.position)

        render_all(entities, game_map=game_map, fov_update=fov_update, camera=camera)

        fov_update = False

        terminal.refresh()
        clear_all(entities)

        action = handle_keys(key)

        move = action.get("move")
        game_exit = action.get("exit", False)

        # if action.get("rebuild"):
        #     random_seed = datetime.now()
        #     print(f"Rebuilding dungeon with new random seed: {random_seed}")
        #     random.seed(random_seed)
        #     dungeon = Dungeon(MAP_SETTINGS)
        #     dungeon.build_dungeon()
        #     game_map = dungeon.game_map
        #     fov_update = True

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities[1:]:
                print(f"The {entity} ponders the meaning of its existence.")

            game_state = GameStates.PLAYER_TURN

        if move and game_state == GameStates.PLAYER_TURN:
            point = player.position + move
            if not game_map.blocked(point):
                target = blocking_entities(entities, point)

                if target:
                    print(f"You kick the {target} in the shins, much to its annoyance!")

                else:
                    player.move(move)

                    fov_update = True

                game_state = GameStates.ENEMY_TURN


if __name__ == "__main__":
    terminal.open()
    terminal.composition(True)
    # logger.add(
    #     "logs/build_maze_{time}.log",
    #     level="ERROR",
    #     format="{time:HH:mm:ss.SSS} {message}",
    # )
    main()
    terminal.close()
