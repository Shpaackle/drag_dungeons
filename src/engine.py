import random
from datetime import datetime
from bearlibterminal import terminal
# from loguru import logger

import const

from entity import Entity
from fov_functions import initialize_fov, update_fov
from handle_keys import handle_keys
from render_functions import render_all, clear_all
from map_objects import DungeonGenerator, Point


class Game:
    def __init__(self, random_seed=None):
        if random_seed is None:
            self.random_seed = datetime.now()
        else:
            self.random_seed = random_seed

        self.dungeon = DungeonGenerator(const.MAP_SETTINGS)

    def on_enter(self):
        random.seed(self.random_seed)
        self.dungeon.build_dungeon()


def main():
    game_exit = False
    random_seed = datetime.now()
    print(random_seed)
    random.seed(random_seed)
    dungeon = DungeonGenerator(const.MAP_SETTINGS)
    dungeon.build_dungeon()

    game_map = dungeon.game_map

    fov_update: bool = True
    initialize_fov(game_map=game_map)

    player = Entity(dungeon.starting_position, char="@", color="white")
    npc = Entity(Point(player.x + 1, player.y + 1), char="@", color="yellow")
    entities = [player, npc]

    terminal.refresh()
    while not game_exit:
        key = None
        if terminal.has_input():
            key = terminal.read()

        if fov_update:
            update_fov(game_map, player.position)

        render_all(entities, game_map=game_map, fov_update=fov_update)

        fov_update = False

        terminal.refresh()
        clear_all(entities)

        action = handle_keys(key)

        move = action.get("move")
        game_exit = action.get("exit", False)

        if move:
            point = player.position + move
            if game_map.walkable[point.x, point.y]:
                player.move(move)

                fov_update = True


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
