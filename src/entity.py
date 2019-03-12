from typing import List

from map_objects import Point


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, name: str, position: Point, char: str, color: str = None, blocks: bool = False):
        if color is None:
            color = "white"
        self.name: str = name
        self.position: Point = position
        self.char: str = char
        self.color: str = color
        self.blocks: bool = blocks

    def __str__(self):
        return self.name

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def move(self, direction: Point):
        self.position += direction


def blocking_entities(entities: List[Entity], point: Point) -> Entity:
    for entity in entities:
        if entity.blocks and entity.position == point:
            return entity

    return None
