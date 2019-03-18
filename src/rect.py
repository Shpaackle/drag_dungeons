from map_objects import Point


# TODO: dataclass?
# TODO: refactor to take kwargs and build Rect from any two points
class Rect:
    def __init__(self, position: Point, width: int, height: int):
        self.position = position
        self.width: int = width
        self.height: int = height

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Point(x=self.x + j, y=self.y + i)

    @property
    def x(self) -> int:
        return self.position.x

    @x.setter
    def x(self, value: int):
        new_position = Point(value, self.y)
        self.position = new_position

    @property
    def y(self) -> int:
        return self.position.y

    @y.setter
    def y(self, value: int):
        new_position = Point(self.x, value)
        self.position = new_position

    @property
    def top_left(self) -> Point:
        return self.position

    @top_left.setter
    def top_left(self, value: Point):
        if self.top_left != value:
            self.position = value

    @property
    def top_right(self) -> Point:
        return Point(self.x + (self.width - 1), self.y)

    @top_right.setter
    def top_right(self, value: Point):
        if value != self.top_right:
            self.position = Point(value.x - (self.width - 1), value.y)

    @property
    def bottom_left(self) -> Point:
        return Point(self.x, self.y + (self.height - 1))

    @property
    def bottom_right(self) -> Point:
        return Point(self.x + (self.width - 1), self.y + (self.height - 1))

    @property
    def right(self) -> int:
        return self.x + (self.width - 1)

    @property
    def bottom(self) -> int:
        return self.y + (self.height - 1)

    @property
    def top(self) -> int:
        return self.y

    @property
    def left(self) -> int:
        return self.x

    @property
    def center(self) -> Point:
        x = self.x + self.width // 2
        y = self.y + self.height // 2
        return Point(x, y)

    @center.setter
    def center(self, point: Point):
        x = point.x - self.width // 2
        y = point.y - self.height // 2
        self.position = Point(x, y)
