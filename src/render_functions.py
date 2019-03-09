import tcod
from bearlibterminal import terminal

from const import Layers
from entity import Entity
from map_objects import Tile, Point, GameMap


def render_all(entities, game_map: GameMap, fov_update: bool,):

    if fov_update:
        terminal.clear()
        terminal.layer(Layers.MAP)

        for point, tile in game_map:
            visible = game_map.fov[point.x, point.y]
            if visible:
                color = terminal.color_from_name("white")
                terminal.color(color)
                game_map.explore(point)
            else:
                color = terminal.color_from_name("grey")
                terminal.color(color)
            if game_map.explored(point):
                terminal.put(point.x, point.y, tile.char)

    for entity in entities:
        draw_entity(entity, game_map)


def draw_entity(entity: Entity, game_map: GameMap):
    if game_map.fov[entity.x, entity.y]:
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
