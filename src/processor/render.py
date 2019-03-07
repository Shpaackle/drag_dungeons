import esper
from bearlibterminal import terminal

import component as c
import const


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
                terminal.put(point.x, point.y, tile.ch)

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
