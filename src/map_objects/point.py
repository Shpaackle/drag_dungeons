from dataclasses import dataclass
from enum import Enum


# TODO: refactor this to class that uses Point?
# class Direction(Enum):
#     NW = (-1, 1)
#     N = (0, 1)
#     NE = (1, 1)
#     W = (-1, 0)
#     E = (1, 0)
#     SW = (-1, -1)
#     S = (0, -1)
#     SE = (1, -1)
#     ORIGIN = (0, 0)


@dataclass(init=True, repr=True, eq=True, order=False, frozen=True)
class Point:
    """
    A simple container to represent a single point in the map's grid
    added functionality for adding, subtracting, or comparing equality of two points
    can be iterated to get x- and y-coordinates

    Args:
        x- and y-coordinate for the point
    """
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Point(self.x * other, self.y * other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        yield self.x
        yield self.y

    @property
    def NW(self):
        return self._direction(Direction.NW.value)

    @property
    def N(self):
        return self._direction(Direction.N.value)

    @property
    def NE(self):
        return self._direction(Direction.NE.value)

    @property
    def W(self):
        return self._direction(Direction.W.value)

    @property
    def E(self):
        return self._direction(Direction.E.value)

    @property
    def SW(self):
        return self._direction(Direction.SW.value)

    @property
    def S(self):
        return self._direction(Direction.S.value)

    @property
    def SE(self):
        return self._direction(Direction.SE.value)

    @property
    def ORIGIN(self):
        return self._direction(Direction.ORIGIN.value)

    def _direction(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def distance(self, point):
        return Point(abs(self.x - point.x), abs(self.y - point.y))

    @property
    def all_neighbors(self):
        for direction in [self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W, self.NW]:
            yield direction

    @property
    def direct_neighbors(self):
        for direction in [self.N, self.E, self.S, self.W]:
            yield direction


class Direction(Enum):
    NW = Point(-1, 1)
    N = Point(0, 1)
    NE = Point(1, 1)
    W = Point(-1, 0)
    E = Point(1, 0)
    SW = Point(-1, -1)
    S = Point(0, -1)
    SE = Point(1, -1)
    ORIGIN = Point(0, 0)
