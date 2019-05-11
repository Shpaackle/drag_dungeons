from bearlibterminal import terminal

from camera import Camera
from const import Layers, Tiles
from entity import Entity
from map_objects import GameMap, Dungeon, Point


def render_all(player, entities, fov_update: bool, camera: Camera, dungeon: Dungeon):
    if fov_update:
        terminal.clear()
        terminal.layer(Layers.MAP)
        dungeon.render_game_map(camera)

    # e_grid = dungeon.entities[camera.left:camera.right, camera.top:camera.bottom]

    player.graphics.render(player.position - camera.top_left)

    for entity in entities:
        if camera.left <= entity.x <= camera.right and camera.top <= entity.y <= camera.bottom:
            if dungeon.can_see(entity, camera):
                point = entity.position - camera.top_left
                entity.graphics.render(point)

    # terminal.printf(0, 20, f"[layer={Layers.UI}]testing messages")


def clear_entity(entity):
    terminal.puts(entity.x, entity.y, f"[layer={entity.layer}][color=white] [/color]")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)

