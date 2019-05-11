from bearlibterminal import terminal as blt


class Graphics:
    def __init__(self):
        self.owner = None

    def render(self, point):
        blt.layer(self.layer)
        blt.puts(point.x, point.y, f"[color={self.color}]{self.char}[/color]")

    @property
    def layer(self):
        return self.owner.layer

    @property
    def color(self):
        return self.owner.color

    @property
    def char(self):
        return self.owner.char
