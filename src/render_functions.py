import tcod
from bearlibterminal import terminal

from const import Layers
from entity import Entity
from map_objects import Tile, Point


def render_all(entities, game_map, fov_update,):

    if fov_update:
        print(f"fov_update = {fov_update}")
        print(f"game_map = {game_map}")
        terminal.clear()
        terminal.layer(Layers.MAP)

        for point, tile in game_map:
            visible = game_map.fov[point.x, point.y]
            print(f"point {point} = {visible}")
            if visible:
                print("visible")
                color = terminal.color_from_name("white")
                terminal.color(color)
            else:
                color = terminal.color_from_name("grey")
                terminal.color(color)
            terminal.put(point.x, point.y, tile.char)

    # if not fov_update:
    #     terminal.clear()
    #     terminal.layer(Layers.MAP)
    #     for y in range(12):
    #         for x in range(9):
    #             if (x == 3 and y == 5) or (x == 9 and y == 7):
    #                 tile = Tile.wall(Point(x, y))
    #             else:
    #                 tile = Tile.floor(Point(x, y))
    #
    #             visible = fov_map.fov[x, y]
    #             print(f"({x}, {y} is visible == {visible}")
    #             if visible:
    #                 color = terminal.color_from_name("white")
    #                 terminal.color(color)
    #             else:
    #                 color = terminal.color_from_argb(100, 100, 100, 100)
    #                 terminal.color(color)
    #             terminal.put(x, y, tile.char)

    for entity in entities:
        draw_entity(entity)


def draw_entity(entity: Entity):
    # set layer to draw on
    terminal.layer(Layers.PLAYER)
    # change color
    color = terminal.color_from_name(entity.color)
    terminal.color(color)
    terminal.put(entity.x, entity.y, entity.char)


def clear_entity(entity):
    terminal.layer(Layers.PLAYER)
    color = terminal.color_from_name(entity.color)
    terminal.color(color)
    terminal.put(entity.x, entity.y, " ")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)


def draw_map(game_map):
    if game_map:
        terminal.layer(Layers.MAP)
        terminal.color(terminal.color_from_name("white"))

        for point, tile in game_map:
            terminal.put(point.x, point.y, tile.char)
