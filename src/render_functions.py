import tcod
from bearlibterminal import terminal

from camera import Camera
from const import Layers, Tiles
from entity import Entity
from map_objects import Tile, Point, GameMap
from rect import Rect


def render_all(entities, game_map: GameMap, fov_update: bool, camera: Camera):

    camera_view = camera.view

    if fov_update:
        terminal.clear()
        terminal.layer(Layers.MAP)

        for x, y, point in camera:
            tile = game_map.tile(point)

            # tile will be displayed
            if tile.visible:
                # tile is currently visible
                color = terminal.color_from_name("white")
                game_map.explore(point)
            else:
                # tile is not
                color = terminal.color_from_name("grey")

            if tile.explored:
                char = tile.char
            else:
                # print(f"{tile.position} is not explored")
                color = terminal.color_from_name("black")
                char = Tiles.UNSEEN

            terminal.color(color)
            terminal.put(x, y, char)
        #
        # for ty in range(camera.height):
        #     for tx in range(camera.width):
        #         point = Point(tx + camera.x, ty + camera.y)
        #         tile = game_map.tile(point)
        #         # color = terminal.color_from_name(tile.color)
        #         color = terminal.color_from_name("white")
        #         terminal.color(color)
        #         terminal.put(tx, ty, tile.char)


                # if not game_map.in_bounds(point) or not game_map.explored(point):
                #     color = "black"
                #     char = Tiles.UNSEEN
                # else:
                #     if game_map.in_fov(point):
                #         color = "white"
                #     else:
                #         color = "grey"
                #     char = game_map.tile(point).char
                # terminal.color(terminal.color_from_name(color))
                # terminal.put(tx, ty, char)
            # terminal.printf(0, ty, row)
        #
        # for point in camera:
        #     if not game_map.in_bounds(point):
        #         continue
        #     visible = game_map.fov[point.x, point.y]
        #     if visible:
        #         color = terminal.color_from_name("white")
        #         terminal.color(color)
        #         game_map.explore(point)
        #     else:
        #         color = terminal.color_from_name("grey")
        #         terminal.color(color)
        #     if game_map.explored(point):
        #         tile = game_map.tile(point)
        #         terminal.put(point.x, point.y, tile.char)

    for entity in entities:
        draw_entity(entity, game_map, camera_view)


def draw_entity(entity: Entity, game_map: GameMap, camera_view: dict):
    if game_map.in_fov(entity.position):
        # set layer to draw on
        terminal.layer(Layers.PLAYER)
        # change color
        color = terminal.color_from_name(entity.color)
        terminal.color(color)
        view_x, view_y = camera_view[entity.position]
        terminal.put(view_x, view_y, entity.char)


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
