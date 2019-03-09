import const
from map_objects import Point, Tile
from map_objects.game_map import GameMap


def initialize_fov(game_map: GameMap):

    for y in range(game_map.height):
        for x in range(game_map.width):
            point = Point(x, y)
            tile: Tile = game_map.tile(point)
            assert game_map.transparent[x, y] == tile.transparent
            assert game_map.walkable[x, y] == tile.walkable


def update_fov(game_map: GameMap, position: Point):
    radius = const.FOV_RADIUS
    game_map.compute_fov(position.x, position.y, radius)
