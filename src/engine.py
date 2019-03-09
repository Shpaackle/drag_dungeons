import esper
import random
from datetime import datetime
from bearlibterminal import terminal
from loguru import logger

import component as c
import const
import processor as p

from entity import Entity
from fov_functions import initialize_fov, update_fov
from handle_keys import handle_keys
from render_functions import render_all, clear_all
from map_objects import DungeonGenerator, Point


# class Game:
#     action = {}
#     game_exit = False
#     map_seed = "TEST_MAP"  # None #
#
#     @classmethod
#     def quit_game(cls):
#         cls.game_exit = True
#
#     def __init__(self):
#         self.world = esper.World()
#         self.dungeon_generator = DungeonGenerator(const.MAP_SETTINGS)
#
#     def on_start(self):
#         processors = (p.MovementProcessor(), p.InputProcessor(), p.RenderProcessor())
#
#         for num, proc in enumerate(processors):
#             self.world.add_processor(proc, priority=num)
#
#     def on_enter(self):
#         random.seed(self.map_seed or datetime.now())
#         player = self.world.create_entity()
#         self.world.add_component(
#             player, c.Position(x=const.SCREEN_WIDTH / 2, y=const.SCREEN_HEIGHT / 2)
#         )
#         self.world.add_component(player, c.Velocity())
#         self.world.add_component(player, c.TakesInput())
#         self.world.add_component(player, c.Renderable())
#         self.world.add_component(player, c.Event({}))
#
#         self.dungeon_generator.build_dungeon()
#
#     def on_update(self):
#         self.world.process(
#             game_map=self.dungeon_generator.tile_map,
#             connections=self.dungeon_generator.connections,
#         )
#         generator = self.world.get_component(c.Event)
#         for ent, event in generator:
#             if event.action.get("exit"):
#                 self.quit_game()
#             if event.action.get("remake"):
#                 self.remake_map()
#
#     def remake_map(self):
#         random.seed(self.map_seed or datetime.now())
#         self.dungeon_generator = DungeonGenerator(const.MAP_SETTINGS)
#         self.dungeon_generator.initialize_map()
#         self.dungeon_generator.build_dungeon()


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


# def old_loop():
#     game = Game()
#     game.on_start()
#     game.on_enter()
#
#     while not game.game_exit:
#         game.on_update()
#
#     player = Entity(Point(10, 10), char="@", color="white")
#     npc = Entity(Point(12, 12), char="@", color="yellow")


if __name__ == "__main__":
    terminal.open()
    terminal.composition(True)
    # logger.add(
    #     "logs/build_maze_{time}.log",
    #     level="ERROR",
    #     format="{time:HH:mm:ss.SSS} {message}",
    # )
    # old_loop()
    main()
    terminal.close()
