import tcod.map

import const
from map_objects import Point, Tile
from map_objects.dungeon import Dungeon


def initialize_fov(game_map: Dungeon):

    for y in range(game_map.height):
        for x in range(game_map.width):
            point = Point(x, y)
            tile = game_map.tile(point)
            assert game_map.transparent[x, y] == tile.transparent
            assert game_map.walkable[x, y] == tile.walkable


def update_fov(game_map: Dungeon, position: Point):
    radius = const.FOV_RADIUS
    game_map.compute_fov(position.x, position.y, radius)
