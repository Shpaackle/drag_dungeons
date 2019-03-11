from map_objects import Point


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, name: str, position: Point, char: str, color: str):
        self.name: str = name
        self.position: Point = position
        self.char: str = char
        self.color: str = color

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    def move(self, direction: Point):
        self.position += direction
