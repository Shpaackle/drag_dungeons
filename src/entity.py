from typing import List, Optional, Dict

from map_objects import Point


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
        print(f"{self} is moving {direction}")
        self.position += direction

    def move_towards(self, target_point, game_map, entity_locations, dungeon):
        dx, dy = target_point - self.position
        distance = target_point.distance(self.position)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        point = Point(self.x + dx, self.y + dy)

        if not (dungeon.blocked(point) or dungeon.entities[point.x, point.y]):
            old_position = self.position
            self.move(Point(dx, dy))
            dungeon.move_entity(entity=self, old_position=old_position, new_position=self.position)

        # if not (game_map.blocked(point) or blocking_entities(entity_locations, point)):
        #     self.move(Point(dx, dy))


def blocking_entities(entity_locations: Dict[Point, List[Entity]], point: Point, dungeon) -> Optional[Entity]:
    entities = entity_locations.get(point, [])
    for entity in entities:
        if entity.blocks:
            return entity

    return None
