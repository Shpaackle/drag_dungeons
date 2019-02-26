import numpy

from typing import Dict, Tuple, Iterable, List

from map_objects.enums import TileType
from map_objects.point import Point
from map_objects.tile import Tile


Grids = Dict[str, int]


class Dungeon:
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width

        self.grid_shape: Tuple[int, int] = (height, width)
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty()).T
        self.tile_map = numpy.zeros(shape=self.grid_shape, dtype=numpy.int).T

        self.label_grid = numpy.zeros(shape=self.grid_shape, dtype=numpy.int).T
        self.blocked_grid = numpy.ones(shape=self.grid_shape, dtype=numpy.int).T
        self.blocks_sight_grid = numpy.ones(shape=self.grid_shape, dtype=numpy.int).T
        self.region_grid = numpy.full(
            shape=self.grid_shape, fill_value=-1, dtype=numpy.int
        ).T

        self.fov_grid = numpy.zeros(shape=self.grid_shape, dtype=numpy.int).T

    @property
    def rows(self):
        return range(self.height)

    @property
    def columns(self):
        return range(self.width)

    def blocked(self, point: Point) -> bool:
        return self.blocked_grid[point.x, point.y] is 1

    def blocks_sight(self, point: Point) -> bool:
        return self.blocks_sight_grid[point.x, point.y] is 1

    def label(self, point: Point) -> int:
        return self.label_grid[point.x, point.y]

    def __iter__(self) -> [Point, Dict[str, int]]:
        for y in self.rows:
            for x in self.columns:
                point = Point(x, y)
                yield point, self.grids(point)

    def clear_dungeon(self):
        """
        Clears the dungeon data by filling the tile grid with empty tiles and region grid with -1
        """
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(
            shape=self.grid_shape, fill_value=-1, dtype=numpy.int
        )
        self.tile_map = numpy.zeros(shape=self.grid_shape, dtype=numpy.int)

        self.label_grid = numpy.zeros(shape=self.grid_shape, dtype=numpy.int).T
        self.blocked_grid = numpy.ones(shape=self.grid_shape, dtype=numpy.int).T
        self.blocks_sight_grid = numpy.ones(shape=self.grid_shape, dtype=numpy.int).T
        self.region_grid = numpy.full(
            shape=self.grid_shape, fill_value=-1, dtype=numpy.int
        ).T

        print(f"After clear, (1, 1) = {self.label(Point(1, 1))}")


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
        self.blocked_grid[x, y] = int(tile.blocked)
        self.blocks_sight_grid[x, y] = int(tile.blocks_sight)
        self.region_grid[x, y] = region

    def grids(self, point: Point) -> Dict[str, int]:
        grids = dict(
            label=self.label(point),
            region=self.region(point),
            blocked=self.blocked(point),
            blocks_sight=self.blocks_sight(point),
        )
        return grids

    def tile(self, point: Point) -> Tile:
        tile = Tile.empty()
        if not self.in_bounds(point):
            return Tile.empty(point)
        try:
            tile_num = self.tile_grid[point.x, point.y]

        except IndexError:
            print(f"{point} out of range")
            return Tile.error(point)
        return tile

    def set_tile(self, point: Point, label: TileType):
        self.tile_grid[point.x, point.y] = Tile.from_label(point, label)

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
