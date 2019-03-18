from bearlibterminal import terminal as blt

from const import Layers, Tiles


class Graphics:
    def __init__(self, char: Tiles, layer: Layers, color: str = "white"):
        self.color = color
        self.char = char
        self.layer = layer

        self.owner = None

    def render(self, point):
        blt.puts(point.x, point.y, f"[layer={self.layer}][color={self.color}]{self.char}[/color]")
