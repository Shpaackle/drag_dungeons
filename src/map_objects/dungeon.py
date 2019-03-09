import numpy
from loguru import logger
from tcod.map import Map
from typing import Dict, Tuple, Iterable, List

from map_objects.point import Point
from map_objects.tile import Tile, TileType

Grids = Dict[str, int]


class Dungeon(Map):
    def __init__(self, height: int, width: int):
        super(Dungeon, self).__init__(width=width, height=height, order="F")
        self.height: int = height
        self.width: int = width

        self.label_grid = numpy.full_like(self.walkable, 0, dtype=numpy.int)
        self.region_grid = numpy.full_like(self.walkable, -1, dtype=numpy.int)

    @property
    def rows(self):
        return range(self.height)

    @property
    def columns(self):
        return range(self.width)

    def blocked(self, point: Point) -> bool:
        return not self.walkable[point.x, point.y]
        # return self.blocked_grid[point.x, point.y]

    def blocks_sight(self, point: Point) -> bool:
        return self.transparent[point.x, point.y]
        # return self.blocks_sight_grid[point.x, point.y]

    def label(self, point: Point) -> int:
        return self.label_grid[point.x, point.y]

    def __iter__(self) -> [Point, Dict[str, int]]:
        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)
                yield point, Tile.from_grid(point, self.grids(point))

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
        # self.blocked_grid[x, y] = int(tile.walkable)
        # self.blocks_sight_grid[x, y] = int(tile.transparent)

    def grids(self, point: Point) -> Dict[str, int]:
        grids = dict(
            label=self.label(point),
            region=self.region(point),
            walkable=self.walkable[point.x, point.y],
            transparent=self.transparent[point.x, point.y],
        )
        return grids

    def tile(self, point: Point) -> Tile:
        tile = Tile.empty()
        if self.in_bounds(point):
            tile = Tile.from_grid(point, self.grids(point))
        return tile

    def region(self, point: Point) -> int:
        return self.region_grid[point.x, point.y]

    def set_region(self, point: Point, region: int):
        self.region_grid[point.x, point.y] = region

    def in_bounds(self, pos: Point) -> bool:
        """
        Checks if position is within the boundaries of the dungeon
        :param pos: position to check
        :type pos: Point
        :return: True is pos is within boundaries of the dungeon
        :rtype: bool
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height
