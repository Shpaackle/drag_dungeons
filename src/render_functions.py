from bearlibterminal import terminal

import const
from entity import Entity


def render_all(entities, game_map=None):
    draw_map(game_map)
    for entity in entities:
        draw_entity(entity)


def draw_entity(entity: Entity):
    # set layer to draw on
    terminal.layer(const.Layers.PLAYER)
    # change color
    color = terminal.color_from_name(entity.color)
    terminal.color(color)
    terminal.put(entity.x, entity.y, entity.char)


def clear_entity(entity):
    terminal.layer(const.Layers.PLAYER)
    color = terminal.color_from_name(entity.color)
    terminal.color(color)
    terminal.put(entity.x, entity.y, " ")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)


def draw_map(game_map):
    if game_map:
        terminal.layer(const.Layers.MAP)
        # terminal.color(terminal.color_from_name("white"))

        for point, tile in game_map:
            terminal.color(terminal.color_from_name("white"))
            terminal.put(point.x, point.y, tile.char)
