from typing import Dict

from const import CAMERA_HEIGHT, CAMERA_WIDTH
from map_objects import Point
from rect import Rect


class Camera(Rect):
    def __init__(self, player, width: int = None, height: int = None):
        # TODO: refactor to remove player and include position
        center = player.position
        if width is None:
            width = CAMERA_WIDTH
        if height is None:
            height = CAMERA_HEIGHT

        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        top_left = Point(center.x - width // 2, center.y - height // 2)

        super(Camera, self).__init__(width=width, height=height, position=top_left)
        self.player = player

    @property
    def x_offset(self) -> int:
        return self.width // 2

    @property
    def y_offset(self) -> int:
        return self.height // 2

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield j, i, Point(x=self.x + j, y=self.y + i)

    @property
    def view_offset(self) -> Dict[Point, Point]:
        view = {}
        for y in range(self.height):
            for x in range(self.width):
                point = Point(self.x + x, self.y + y)
                view[point] = Point(x, y)

        return view

    def recenter(self, point: Point):
        """Centers camera on point provided"""
        x = point.x - self.width // 2
        y = point.y - self.height // 2
        self.position = Point(x, y)
