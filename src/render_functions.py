from bearlibterminal import terminal

from camera import Camera
from const import Layers, Tiles
from entity import Entity
from map_objects import GameMap, Dungeon


def render_all(entities, fov_update: bool, camera: Camera, dungeon: Dungeon):
    if fov_update:
        terminal.clear()
        terminal.layer(Layers.MAP)
        dungeon.render_game_map(camera)

    for entity in entities:
        if dungeon.can_see(entity=entity, view=camera):
            point = entity.position - camera.top_left
            entity.graphics.render(point)


def clear_entity(entity):
    terminal.puts(entity.x, entity.y, f"[layer={Layers.PLAYER}][color=white] [/color]")


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)

