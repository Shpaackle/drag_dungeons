from bearlibterminal import terminal

from camera import Camera
from const import Layers, Tiles
from entity import Entity
from map_objects import GameMap, Dungeon, Point


def render_all(player, entities, fov_update: bool, camera: Camera, dungeon: Dungeon, test=False):
    if fov_update:
        terminal.clear()
        terminal.layer(Layers.MAP)
        dungeon.render_game_map(camera, test=test)

    # e_grid = dungeon.entities[camera.left:camera.right, camera.top:camera.bottom]

    player.graphics.render(player.position - camera.top_left)

    for entity in entities:
        if camera.left <= entity.x <= camera.right and camera.top <= entity.y <= camera.bottom:
            if dungeon.can_see(entity, camera):
                point = entity.position - camera.top_left
                entity.graphics.render(point)

    # for col in range(camera.height):
    #     for row in range(camera.width):
    #         try:
    #             entity = e_grid[row, col]
    #         except IndexError:
    #             print(f"Index error {row, col}")
    #             continue
    #         if entity:
    #             if dungeon.can_see(entity, view=camera):
    #                 point = entity.position - camera.top_left
    #                 print(f"{entity} at {entity.position} is at terminal {point}")
    #                 entity.graphics.render(entity.position - camera.top_left)
    #             terminal.puts(entity.x - camera.x, entity.y - camera.y, f"[color=red][layer=30] [/color][/layer]")
    #             # else:
                #     print(f"{entity} at {entity.position} did not get drawn")

    # for entity in iter(entities):
    #     if dungeon.can_see(entity=entity, view=camera):
    #         point = entity.position - camera.top_left
    #         entity.graphics.render(point)


def clear_entity(entity):
    terminal.puts(entity.x, entity.y, f"[layer={Layers.PLAYER}][color=white] [/color]")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)

