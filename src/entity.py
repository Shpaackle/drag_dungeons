from typing import List, Optional, Dict

from bearlibterminal import terminal as blt
import tcod.path

from const import Layers
from map_objects import Point
from map_objects.a_star import find_path


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(
        self,
        name: str,
        position: Point,
        char: str,
        color: str = None,
        blocks: bool = False,
        fighter=None,
        ai=None,
        graphics=None,
    ):
        if color is None:
            color = "white"
        self.name: str = name
        self.position: Point = position
        self.char: str = char
        self.color: str = color
        self.blocks: bool = blocks
        self.fighter = fighter
        self.ai = ai
        self.graphics = graphics
        self.layer = Layers.PLAYER

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.graphics:
            self.graphics.owner = self

    def __str__(self):
        return self.name

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def move(self, direction: Point):
        # print(f"{self} is moving {direction}")
        self.position += direction

    def move_towards(self, target_point, game_map, entity_locations, dungeon):
        dx, dy = target_point - self.position
        distance = target_point.distance(self.position)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        point = Point(self.x + dx, self.y + dy)

        blocked = dungeon.blocked(point)
        for entity in dungeon.entities:
            if entity.position == point:
                blocked = entity.blocks

        if not blocked:
            old_position = self.position
            self.move(Point(dx, dy))
            # dungeon.move_entity(entity=self, old_position=old_position, new_position=self.position)

        # if not (game_map.blocked(point) or blocking_entities(entity_locations, point)):
        #     self.move(Point(dx, dy))

    def move_a_star(self, target, dungeon, entity_locations):
        # walkable = dungeon.game_map.walkable
        # for entity in dungeon.entities:
        #     if entity.blocks:
        #         walkable[entity.x, entity.y] = False
        astar = tcod.path.AStar(dungeon.path_blocking)
        path = astar.get_path(self.x, self.y, target.x, target.y)
        if path and len(path) < 25:
            destination = path[0]
            direction = Point(destination[0], destination[1]) - self.position
            self.move(direction)
            # dungeon.move_entity(entity=self, old_position=old_position, new_position=self.position)
        else:
            self.move_towards(target.position, entity_locations=entity_locations, dungeon=dungeon, game_map=dungeon.game_map)


def blocking_entities(entity_locations: Dict[Point, List[Entity]], point: Point, dungeon) -> Optional[Entity]:
    entities = entity_locations.get(point, [])
    for entity in entities:
        if entity.blocks:
            return entity

    return None
