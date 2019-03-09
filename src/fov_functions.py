import tcod.map

import const
from map_objects import Point, Tile
from map_objects.dungeon import Dungeon


def initialize_fov(game_map: Dungeon, testing=False):

    if testing:
        m = tcod.map.Map(width=9, height=12, order="F")
        print(f"walkable = {m.walkable}")

        for y in range(12):
            for x in range(9):
                if (x == 3 and y == 5) or (x == 9 and y ==7):
                    tile = Tile.wall(Point(x, y))
                else:
                    tile = Tile.floor(Point(x, y))

                m.walkable[x, y] = tile.walkable
                m.transparent[x, y] = tile.transparent
        return m

    # fov_map = tcod.map.Map(width=const.MAP_SETTINGS["map_width"], height=const.MAP_SETTINGS["map_height"], order="F")
    #
    # for point, tile in game_map:
    #     fov_map.transparent[point.x, point.y] = tile.transparent
    #     fov_map.walkable[point.x, point.y] = tile.walkable
    #     # tcod.map_set_properties(fov_map, point.x, point.y, not tile.transparent, not tile.walkable)
    #
    # return fov_map

    for y in range(game_map.height):
        for x in range(game_map.width):
            point = Point(x, y)
            tile = game_map.tile(point)
            assert game_map.transparent[x, y] == tile.transparent
            assert game_map.walkable[x, y] == tile.walkable


def update_fov(game_map: Dungeon, position: Point):
    radius = const.FOV_RADIUS
    game_map.compute_fov(position.x, position.y, radius)
