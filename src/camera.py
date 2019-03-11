from entity import Entity
from map_objects import Point
from rect import Rect
from const import CAMERA_HEIGHT, CAMERA_WIDTH


class Camera:
    def __init__(self, player: Entity, width: int = None, height: int = None):
        self.player = player
        if width is None:
            self.width = CAMERA_WIDTH
        else:
            self.width = width
        if height is None:
            self.height = CAMERA_HEIGHT
        else:
            self.height = height

    @property
    def x_offset(self) -> int:
        return self.width // 2

    @property
    def y_offset(self) -> int:
        return self.height // 2

    @property
    def x(self):
        return self.player.x - self.x_offset

    @property
    def y(self):
        return self.player.y - self.y_offset

    @property
    def position(self) -> Point:
        return Point(self.x - self.x_offset, self.y - self.y_offset)

    @property
    def center(self) -> Point:
        return self.player.position

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield j, i, Point(x=self.x + j, y=self.y + i)

    @property
    def top_left(self) -> Point:
        return Point(self.x, self.y)

    @property
    def bottom_left(self) -> Point:
        return self.player.position + self.offset

    @property
    def offset(self) -> Point:
        return Point(self.x_offset, self.y_offset)

    @property
    def view(self) -> dict:
        view = {}
        for x, y, point in iter(self):
            view[point] = Point(x, y)

        return view
