import tcod


def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for point, tile in game_map:
        tcod.map_set_properties(fov_map, point.x, point.y, not tile.blocks_sight, not tile.blocked)

    return fov_map
