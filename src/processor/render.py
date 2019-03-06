import esper
from bearlibterminal import terminal

import component as c
import const

from map_objects.tile import TileType


class RenderProcessor(esper.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

        self.screen_width = const.SCREEN_WIDTH
        self.screen_height = const.SCREEN_HEIGHT
        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT

    def process(self, **kwargs):
        self.render_all()
        self.render_map(kwargs.get("game_map"))
        self.render_test_map(kwargs.get("game_map"), kwargs.get("connections"))
        self.refresh_terminal()
        self.clear_all()

    def render_map(self, game_map):
        if game_map:
            terminal.layer(const.Layers.MAP)
            terminal.color(terminal.color_from_name("white"))
            for point, tile in game_map:
                # color = terminal.color_from_name("white")
                # ch = const.Tiles.UNSEEN
                # if tile.label == TileType.EMPTY:
                #     color = terminal.color_from_name("black")
                #     # ch = const.Tiles.UNSEEN
                # elif tile.label == TileType.FLOOR:
                #     color = terminal.color_from_name("grey")
                #     ch = const.Tiles.FLOOR
                # elif tile.label == TileType.WALL:
                #     color = terminal.color_from_name("black")
                #     ch = const.Tiles.WALL
                # elif tile.label == TileType.CORRIDOR:
                #     color = terminal.color_from_name("dark_grey")
                #     ch = const.Tiles.CORRIDOR
                # terminal.bkcolor(color)
                #terminal.color(terminal.color_from_name("white"))
                terminal.put(point.x, point.y, tile.ch)

        # terminal.put(1, 1, "\uE003")
        # terminal.color(terminal.color_from_name("white"))

    def render_test_map(self, game_map, connections):
        if game_map and connections:
            terminal.layer(const.Layers.TESTING)
            for point in connections:
                terminal.color(terminal.color_from_name("blue"))
                terminal.put(point.x, point.y, const.Tiles.BLOCK)

    def render_all(self):
        generator = self.world.get_components(c.Renderable, c.Position)

        for ent, (rend, pos) in generator:
            color = terminal.color_from_argb(255, r=rend.fg[0], g=rend.fg[1], b=rend.fg[2])
            terminal.layer(const.Layers.PLAYER)
            terminal.color(color)
            terminal.put(x=int(pos.x), y=int(pos.y), c=rend.ch)

    @staticmethod
    def refresh_terminal():
        terminal.refresh()

    @staticmethod
    def clear_all():
        terminal.clear()
