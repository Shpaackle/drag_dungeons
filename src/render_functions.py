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

    for col in range(camera.height):
        for row in range(camera.width):
            try:
                entity = dungeon.entities[row, col]
            except IndexError:
                continue
            if entity:
                if dungeon.can_see(entity, view=camera):
                    entity.graphics.render(entity.position - camera.top_left)

    # for entity in iter(entities):
    #     if dungeon.can_see(entity=entity, view=camera):
    #         point = entity.position - camera.top_left
    #         entity.graphics.render(point)


def clear_entity(entity):
    terminal.puts(entity.x, entity.y, f"[layer={Layers.PLAYER}][color=white] [/color]")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)

