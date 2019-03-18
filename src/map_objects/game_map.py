from typing import Dict

import numpy
from tcod.map import Map

from map_objects.point import Point
from map_objects.tile import Tile

Grids = Dict[str, int]


class GameMap(Map):
    def __init__(self, height: int, width: int):
        super(GameMap, self).__init__(width=width, height=height, order="F")
        self.height: int = height
        self.width: int = width

        self.label_grid = numpy.full_like(self.walkable, 0, dtype=numpy.int)
        self.region_grid = numpy.full_like(self.walkable, -1, dtype=numpy.int)

        self.explored_grid = numpy.full_like(self.walkable, False, dtype=numpy.bool)

    @property
    def rows(self):
        return range(self.height)

    @property
    def columns(self):
        return range(self.width)

    def in_fov(self, point: Point) -> bool:
        try:
            return self.fov[point.x, point.y]
        except IndexError:
            print(f"point {point} outside of fov_grid")
            print(f"height = {self.height}, width = {self.width}")
            print(f"fov grid_shape = {self.fov.shape}")
            return True

    def blocked(self, point: Point) -> bool:
        if not self.in_bounds(point):
            return False
        return not self.walkable[point.x, point.y]

    def blocks_sight(self, point: Point) -> bool:
        return self.transparent[point.x, point.y]

    def label(self, point: Point) -> int:
        return self.label_grid[point.x, point.y]

    def explored(self, point: Point) -> bool:
        return self.explored_grid[point.x, point.y]

    def __iter__(self) -> [Point, Dict[str, int]]:
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                yield point, Tile.from_grid(point, self.grids(point))

    # TODO: remove region in place, set region at place() call instead
    def place(self, point: Point, tile: Tile, region: int):
        """
        assigns grid values for Tile at point with region
        :param point:
        :type point:
        :param tile:
        :type tile:
        :param region:
        :type region:
        :return:
        :rtype:
        """
        x, y = point
        self.label_grid[x, y] = tile.label.value
        self.walkable[x, y] = tile.walkable
        self.transparent[x, y] = tile.transparent
        self.region_grid[x, y] = region

    def grids(self, point: Point) -> Dict[str, int]:
        grids = dict(
            label=self.label(point),
            region=self.region(point),
            walkable=self.walkable[point.x, point.y],
            transparent=self.transparent[point.x, point.y],
            visible=self.in_fov(point),
            explored=self.explored(point)
        )
        return grids

    def tile(self, point: Point) -> Tile:
        tile = Tile.empty(point)
        if self.in_bounds(point):
            tile = Tile.from_grid(point, self.grids(point))
        return tile

    def region(self, point: Point) -> int:
        return self.region_grid[point.x, point.y]

    def in_bounds(self, point: Point) -> bool:
        """
        Checks if point is within the boundaries of the game map
        :param point: point to check
        :type point: Point
        :return: True if point is within boundaries of the game map
        :rtype: bool
        """
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def explore(self, point: Point):
        """
        sets explored_grid at point to True
        :param point: point in game map to mark explored
        :type point: Point
        :return: None
        :rtype: None
        """
        if not self.explored(point):
            self.explored_grid[point.x, point.y] = True
