import numpy as np

from bearlibterminal import terminal as blt
from collections import defaultdict, OrderedDict
from loguru import logger
from random import randint, randrange, choice
from typing import Dict, Iterable, List, Set, Tuple

from components import Fighter, BasicMonster, Graphics
from const import Tiles, Layers
from entity import Entity
from map_objects.game_map import GameMap
from map_objects.enums import Direction
from map_objects.point import Point
from map_objects.tile import Tile, TileType
from map_objects.kruskal import Graph
from rect import Rect


class RegionGraph:
    def __init__(self, vertices: int, main_region: int):
        self.V = vertices

        self.adj_matrix = np.zeros((vertices, vertices), dtype=np.int)
        self.connected_matrix = np.zeros_like(self.adj_matrix)
        for i in range(vertices):
            self.adj_matrix[i, i] = 1
            self.connected_matrix[i, i] = 1

        self.edge_points: Dict[Tuple[int, int], List[Point]] = defaultdict(list)
        self._main_region = main_region
        self.connection_points: Set[Point] = set()

    def add_edge(self, v1: int, v2: int, connection: Point = None):
        self.adj_matrix[v1, v2] = 1
        self.adj_matrix[v2, v1] = 1
        self.edge_points[(min(v1, v2), max(v1, v2))].append(connection)

    def remove_edge(self, v1: int, v2: int):
        self.adj_matrix[v1, v2] = 0
        self.adj_matrix[v2, v1] = 0
        # del self.edge_points[(min(v1, v2), max(v1, v2))]

    def join_regions(self, v1: int, point: Point):
        for v2 in self.merged_regions:
            self.connected_matrix[v1, v2] = 1
            self.connected_matrix[v2, v1] = 1
            self.remove_edge(v1, v2)
        self.connection_points.add(point)

    def find_neighbors(self, v1: int):
        for v2 in range(self.V):
            if self.adj_matrix[v1, v2] == 1:
                yield v2

    def find_connections(self, v1: int) -> Iterable[int]:
        for v2 in range(self.V):
            if self.connected_matrix[v1, v2] == 1:
                yield v2

    @property
    def merged_regions(self) -> Set[int]:
        return set(self.find_connections(self._main_region))


class Room(Rect):
    """
    Args:
        x- and y-coordinate of the top left corner of the room
        width and height of the room

    Attributes:
        x, y: top left coordinate in the 2d array
        width: number of tiles the room spans
        height: number of tiles the room spans
        region: number corresponding to region, used for connecting locations
        connections: list of regions room is connected to
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        super(Room, self).__init__(Point(x, y), width, height)
        # self.x: int = x
        # self.y: int = y
        # self.width: int = width
        # self.height: int = height
        self.region: int = None
        self.connections: list = []

    # def __iter__(self):
    #     for i in range(self.height):
    #         for j in range(self.width):
    #             yield Point(x=self.x + j, y=self.y + i)

    # @property
    # def top_left(self) -> Point:
    #     return Point(self.x, self.y)
    #
    # @property
    # def top_right(self) -> Point:
    #     return Point(self.x + self.width - 1, self.y)
    #
    # @property
    # def bottom_left(self) -> Point:
    #     return Point(self.x, self.y + self.height - 1)
    #
    # @property
    # def bottom_right(self) -> Point:
    #     return Point(self.x + self.width - 1, self.y + self.height - 1)
    #
    # @property
    # def right(self) -> int:
    #     return self.x + self.width - 1
    #
    # @property
    # def bottom(self) -> int:
    #     return self.y + self.height - 1


class Dungeon:
    def __init__(self, map_settings: dict):

        self.game_map = GameMap(
            height=map_settings["map_height"], width=map_settings["map_width"]
        )

        self.current_region: int = -1

        self.rooms: List[Room] = []
        self.corridors: List[Point] = []

        self.connections = []

        self.map_settings = OrderedDict(map_settings)
        self.winding_percent: int = 20

        self.seed = None

        self.region_graph = None
        self.connector_regions = None
        self.joined_regions = None

        self.entities = None

    @property
    def starting_position(self) -> Point:
        return self.rooms[0].top_left

    # @property
    # def game_map(self):
    #     return self.game_map

    # @property
    # def tile_map(self):
    #     for point, tile in self.game_map:
    #         yield point, tile

    @property
    def max_rooms(self):
        return self.map_settings["num_rooms"]

    def new_region(self) -> int:
        """
        increases current_region by 1 and then returns current_region
        """
        self.current_region += 1
        return self.current_region

    def initialize_map(self):
        for y in self.game_map.rows:
            for x in self.game_map.columns:
                self.game_map.place(Point(x, y), Tile.wall(Point(x, y)), region=-1)

    # TODO: refactor self.tile to take Point
    def tile(self, x: int, y: int) -> Tile:
        """

        :param x: x-coordinate of tile
        :type x: int
        :param y: y-coordinate of tile
        :type y: int
        :return: Tile at coordinate (x, y)
        :rtype: Tile
        """

        grids = self.game_map.grids(Point(x, y))
        tile = Tile.from_grid(Point(x, y), grids)

        return tile

    # TODO: replace start_x and start_y with Point variable
    def place_room(
        self,
        start_x: int,
        start_y: int,
        room_width: int,
        room_height: int,
        margin: int,
        ignore_overlap: bool = False,
    ):
        """

        :param start_x: 
        :type start_x: int
        :param start_y: 
        :type start_y: int
        :param room_width: 
        :type room_width: int
        :param room_height: 
        :type room_height: int
        :param margin: 
        :type margin: int
        :param ignore_overlap: 
        :type ignore_overlap: bool
        """
        room = Room(start_x, start_y, room_width, room_height)
        if self.room_fits(room, margin) or ignore_overlap:
            region = self.new_region()
            room.region = region
            for point in room:

                tile = Tile.floor(point)
                self.game_map.place(point, tile, region)

            self.rooms.append(room)

    def place_random_rooms(
        self,
        min_room_size: int,
        max_room_size: int,
        room_step: int = 2,
        margin: int = None,
        attempts: int = 1000,
    ):
        """

        :param min_room_size: minimum number of tiles
        :type min_room_size: int
        :param max_room_size: 
        :type max_room_size: int
        :param room_step: 
        :type room_step: int
        :param margin: 
        :type margin: int
        :param attempts: number of times 
        :type attempts: int
        """
        if margin is None:
            margin = self.map_settings["room_margin"]
        for _ in range(attempts):
            if len(self.rooms) >= self.max_rooms:
                break
            room_width = randrange(min_room_size, max_room_size, room_step)
            room_height = randrange(min_room_size, max_room_size, room_step)
            start_point = self.random_point()
            self.place_room(
                start_point.x, start_point.y, room_width, room_height, margin
            )

    def room_fits(self, room: Room, margin: int, simple: bool = False) -> bool:
        """

        :param room: 
        :type room: Room
        :param margin: 
        :type margin: int
        :return: 
        :rtype: bool
        """
        mar_room = Room(
            (room.x - margin),
            (room.y - margin),
            (room.width + margin * 2),
            (room.height + margin * 2),
        )

        if (
            mar_room.x + mar_room.width < self.width
            and mar_room.y + mar_room.height < self.height
            and mar_room.x >= 0
            and mar_room.y >= 0
        ):
            for x, y in mar_room:
                tile = self.tile(x, y)
                if tile.label is not TileType.WALL:
                    return False

            return True
        return False

    def grow_maze(self, start: Point, label: TileType = None):
        """

        :param start:
        :type start: Point
        :param label:
        :type label: map_objects.tile.TileType
        """

        if label is None:
            label = TileType.CORRIDOR
        tiles = []  # tiles to check
        last_direction = Point(0, 0)

        if not self.can_place(start, last_direction):
            return
        region = self.new_region()

        self.place_tile(start, region=region, label=label)
        self.corridors.append(start)

        tiles.append(start)

        while len(tiles) > 0:

            tile = tiles[-1]  # grab last tile

            # see which neighboring tiles can be carved
            open_tiles = []

            for d in Direction.cardinal():

                if self.can_place(tile, d):

                    open_tiles.append(d)

            if len(open_tiles) > 0:

                if (
                    last_direction in open_tiles
                    and randint(1, 101) > self.winding_percent
                ):

                    current_direction = last_direction

                else:
                    # TODO: refactor for random.choice()
                    current_direction = open_tiles[randint(0, len(open_tiles) - 1)]

                self.place_tile(tile + current_direction, region=region, label=label)
                self.corridors.append(tile + current_direction)

                tiles.append(tile + current_direction)  # * 2)
                last_direction = current_direction
            else:
                tiles.remove(tile)
                last_direction = None

    def find_neighbors(self, point: Point, neighbors: Direction = None):
        """

        used by find_direct_neighbors
        :param point:
        :type point: Point
        :param neighbors: direction for neighbors to check, defaults to None
        :type neighbors: Direction
        :return yields new point in direction(s) chosen
        """
        if neighbors is None:
            neighbors = Direction.every()
        for direction in neighbors:
            new_point = point + direction
            if not self.game_map.in_bounds(new_point):
                continue
            yield new_point

    def find_direct_neighbors(self, point: Point):
        """
        used by possible_moves
        :param point:
        :type point:
        :return:
        :rtype:
        """
        return self.find_neighbors(point, neighbors=Direction.cardinal())

    # def clear_map(self):
    #     """
    #     Clears map by setting rooms to an empty list and calling game_map.clear_dungeon()
    #     """
    #     self.rooms = []
    #
    #     self.game_map.clear_dungeon()

    def can_carve(self, pos: Point, direction: Point) -> bool:

        if pos is None:
            print("pos in can_carve() sent as None")
            return False

        xs = (1, 0, -1) if direction.x == 0 else (1 * direction.x, 2 * direction.x)
        ys = (1, 0, -1) if direction.y == 0 else (1 * direction.y, 2 * direction.y)

        for x in xs:
            for y in ys:
                if self.width <= pos.x + x or self.height <= pos.y + y:
                    return False
                tile = self.tile(pos.x + x, pos.y + y)
                if tile.label != TileType.WALL:
                    return False
        return True

    def carve(self, point: Point, region: int, label: TileType = TileType.FLOOR):

        tile = Tile.from_label(point, label)
        self.game_map.place(point, tile, region)

    def build_corridors(self, start_point: Point = None):
        cells = []
        if start_point is None:
            start_point = Point(
                x=randint(1, self.width - 2), y=randint(1, self.height - 2)
            )
            # TODO: refactor can_carve
        attempts = 0
        while not self.can_carve(start_point, Direction.self()):
            attempts += 1
            start_point = Point(
                x=randint(1, self.width - 2), y=randint(1, self.height - 2)
            )
            # TODO: need to remove this hard stop once everything is combined
            if attempts > 100:
                break

        self.carve(point=start_point, region=self.new_region(), label=TileType.CORRIDOR)
        # add point to corridor list
        self.corridors.append(start_point)
        # add point to open cell list
        cells.append(start_point)

        while cells:
            middle = len(cells) // 2
            start_point = cells[-1]
            possible_moves = self.possible_moves(start_point)
            if possible_moves:
                point = choice(possible_moves)
                self.carve(
                    point=point, region=self.current_region, label=TileType.CORRIDOR
                )
                self.corridors.append(point)
                cells.append(point)
            else:
                cells.remove(start_point)

    def possible_moves(self, pos: Point) -> List[Point]:
        """
        searches for directions that a corridor can expand
        used by build_corridors()
        :param pos: index of tile in grid to find possible moves
        :type pos: Point
        :return: list of potential points the path could move
        :rtype: List[Point]
        """

        available_squares = []
        for direction in Direction.cardinal():

            neighbor = pos + direction

            if (
                neighbor.x < 1
                or self.width - 2 < neighbor.x
                or neighbor.y < 1
                or self.height - 2 < neighbor.y
            ):

                continue
            if self.can_carve(pos, direction):

                available_squares.append(neighbor)

        return available_squares

    @property
    def width(self) -> int:
        return self.map_settings["map_width"]

    @property
    def height(self) -> int:
        return self.map_settings["map_height"]

    def random_point(self) -> Point:
        return Point(
            x=randint(0, self.game_map.width), y=randint(0, self.game_map.height)
        )

    def build_dungeon(self):
        self.initialize_map()
        self.place_random_rooms(
            min_room_size=self.map_settings["min_room_size"],
            max_room_size=self.map_settings["max_room_size"],
        )

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                point = Point(x, y)
                if self.game_map.label(point) != TileType.WALL.value:
                    continue
                self.grow_maze(point)

        self.connect_regions()

        self.remove_dead_ends()

    def find_empty_space(self, distance: int) -> Point:
        for x in range(distance, self.width - distance):
            for y in range(distance, self.height - distance):
                touching = 0
                for xi in range(-distance, distance):
                    for yi in range(-distance, distance):
                        if self.game_map.label(Point(x + xi, y + yi)):
                            touching += 1
                if touching == 0:
                    print(f"returning {Point(x, y)}")
                    return Point(x, y)
        print("returning no point")
        return Point(-1, -1)

    # TODO: Refactor get_extents
    def get_extents(self, point: Point, direction: Point):
        if direction == Point(0, 0):
            return point.NW, point.SE
        # north
        elif direction == Point(0, 1):
            return point.N.NW, point.NE
        # east
        elif direction == Point(1, 0):
            return point.NE, point.E.SE
        # west
        elif direction == Point(-1, 0):
            return point.W.NW, point.SW
        # south
        elif direction == Point(0, -1):
            return point.SW, point.S.SE
        else:
            print("get_extents else statement")
            print(f"Direction not valid: point={point}, direction={direction}")

    @logger.catch()
    def place_tile(self, point: Point, label: TileType, region: int):
        tile = Tile.from_label(point, label)
        x, y = point
        self.game_map.label_grid[x, y] = label.value
        self.game_map.walkable[x, y] = tile.walkable
        self.game_map.transparent[x, y] = tile.transparent
        self.game_map.region_grid[x, y] = region

    @logger.catch()
    def can_place(self, point: Point, direction: Point) -> bool:
        top_left, bottom_right = self.get_extents(point, direction)

        return (
            self.game_map.in_bounds(top_left)
            and self.game_map.in_bounds(bottom_right)
            and self.are_walls(top_left, bottom_right)
        )

    def are_walls(self, top_left, bottom_right):
        for x in range(top_left.x, bottom_right.x + 1):
            for y in range(bottom_right.y, top_left.y + 1):
                if self.game_map.label_grid[x, y] != 0:
                    return False
        return True

    def find_connectors(self):
        connector_regions = dict()
        for point, tile in self.game_map:
            if tile.label != TileType.WALL:
                continue

            regions = set()

            for neighbor in [point.N, point.E, point.W, point.S]:
                if not self.game_map.in_bounds(neighbor):
                    continue
                region = self.game_map.region(neighbor)
                if region > -1:
                    regions.add(region)

            if len(regions) < 2:
                continue

            connector_regions[point] = regions
        return connector_regions

    def connect_regions(self):
        # self.joined_regions = set()
        connector_regions = self.find_connectors()

        regions_connectors = defaultdict(list)
        region_neighbors = defaultdict(list)
        for c, (r1, r2) in connector_regions.items():
            region_pair = (min(r1, r2), max(r1, r2))
            regions_connectors[region_pair].append(c)
            region_neighbors[r1].append(r2)
            region_neighbors[r2].append(r1)

        all_connectors = list(connector_regions.keys())

        # choose random room to begin set for main region
        start_region = randint(0, len(self.rooms))
        # initialize region graph
        g = RegionGraph(self.current_region + 1, start_region)
        # add edges to graph
        for p, (r1, r2) in connector_regions.items():
            g.add_edge(r1, r2, p)

        while all_connectors:

            neighbors = [n for r in g.merged_regions for n in g.find_neighbors(r)]

            # choose random neighbor
            neighbor = choice(neighbors)
            # get connecting points between merged regions and neighbor
            poss_connections = [
                point
                for r in g.merged_regions
                for point in regions_connectors[(min(r, neighbor), max(r, neighbor))]
            ]
            # choose random connecting point
            if poss_connections:
                chosen_connection = choice(poss_connections)
                # place connection at point connecting the regions
                self.place_connection(chosen_connection, start_region)
                # add neighbor to merged region
                g.join_regions(neighbor, chosen_connection)
            else:
                print(f"poss_connections was empty, neighbor={neighbor}")
                chosen_connection = Point(0, 0)
            # for every point all connectors
            remove_list = set()
            for point in all_connectors:
                r1, r2 = connector_regions.get(point, [-1, -1])
                if point.distance(chosen_connection) <= 1:
                    pass
                elif r1 in g.merged_regions and r2 in g.merged_regions:
                    if randint(0, self.map_settings["extra_door_chance"]) == 0:
                        self.place_connection(chosen_connection, start_region)
                        g.join_regions(r1, point)
                        g.join_regions(r2, point)
                else:
                    # still not connected to merged region
                    continue
                remove_list.add(point)
            for p in remove_list:
                if p in all_connectors:
                    all_connectors.remove(p)
                else:
                    print(f"failed to remove {p} from all_connectors")

        joined_regions = {c for c in g.find_connections(start_region)}

        if len(joined_regions) != self.current_region + 1:
            print(f"current_region = {self.current_region}")
            print(f"joined regions = {joined_regions}")

        self.region_graph = g
        self.connector_regions = connector_regions

        # self.min_spanning_tree()
        # region_tree = self.region_graph.result
        # for point, r1, r2, _ in region_tree:
        #     self.place_connection(point, r1)
        #     self.joined_regions.add(r2)

        # for region in range(self.current_region):
        #     if region not in self.joined_regions:
        #         print(f"region {region} not joined, but why?")

    def place_connection(self, point, region):
        # if random.randint(1, 4) == 1:
        #     label = TileType.DOOR_OPEN
        # else:
        #     label = TileType.DOOR_CLOSED
        # TODO: undo commented code when doors work
        label = TileType.DOOR_OPEN
        self.place_tile(point, label, region)

    def get_unconnected_regions(self, connector_regions):
        """ returns a set of unconnected regions """
        regions = set()
        for r1, r2 in connector_regions.values():
            regions.add(r1)
            regions.add(r2)

        return [region for region in regions if region not in self.joined_regions]

    def min_spanning_tree(self):
        points = self.connector_regions.copy()
        v = len(self.get_unconnected_regions(points))
        g = Graph(v)
        for point, (r1, r2) in points.items():
            g.add_edge(point, r1, r2, 1)
        g.kruskal_MST()
        self.region_graph = g

    def remove_dead_ends(self):
        dead_ends = self.dead_ends
        while dead_ends:
            point = dead_ends.pop(-1)
            self.place_tile(point, TileType.WALL, -1)
            self.corridors.remove(point)

            dead_ends = self.dead_ends

    @property
    def dead_ends(self):
        dead_ends = []
        # iterate through corridors
        for point in self.corridors:
            walls = 0
            for neighbor in point.direct_neighbors:
                tile = self.tile(*neighbor)
                if tile.label == TileType.WALL:
                    walls += 1
            if walls >= 3:
                dead_ends.append(point)

        return dead_ends

    def is_blocked(self, point: Point) -> bool:
        if self.game_map.blocked(point):
            return True

        return False

    def place_entities(self, player: Entity) -> List[Entity]:
        max_monsters_per_room = self.map_settings["max_monsters_per_room"]

        self.entities = [player]

        for room in self.rooms[1:]:
            number_of_monsters = randint(0, max_monsters_per_room)

            for i in range(number_of_monsters):
                x = randint(room.left, room.right)
                y = randint(room.top, room.bottom)
                point = Point(x, y)

                if not any(
                    [entity for entity in self.entities if entity.position == point]
                ):
                    if randint(0, 100) < 80:
                        fighter_component = Fighter(hp=10, defense=0, power=3)
                        ai_component = BasicMonster()
                        graphics_component = Graphics(
                            char=Tiles.GOBLIN, layer=Layers.PLAYER
                        )
                        monster = Entity(
                            name="goblin",
                            position=point,
                            char=Tiles.GOBLIN,
                            blocks=True,
                            fighter=fighter_component,
                            ai=ai_component,
                            graphics=graphics_component,
                        )
                    else:
                        ai_component = BasicMonster()
                        fighter_component = Fighter(hp=16, defense=1, power=4)
                        graphics_component = Graphics(
                            char=Tiles.ORC, layer=Layers.PLAYER
                        )
                        monster = Entity(
                            name="orc",
                            position=point,
                            char=Tiles.ORC,
                            blocks=True,
                            fighter=fighter_component,
                            ai=ai_component,
                            graphics=graphics_component,
                        )

                    self.entities.append(monster)

        return self.entities

    def maps(self, position: Point, width: int, height: int) -> dict:
        x1, y1 = position
        x2 = position.x + width
        y2 = position.y + height
        fov_map = self.game_map.fov[x1:x2, y1:y2]
        tile_map = np.array((height, width))
        # for y in range()
        return {}

    def tile_map(self, x1: int, y1: int, width: int, height: int):
        for y in range(y1, y1 + height):
            for x in range(x1, x1 + width):
                yield Point(x, y), self.tile(x, y)

    def render_game_map(self, camera: Rect, test=False):
        for row, y in enumerate(range(camera.y, camera.bottom)):
            for col, x in enumerate(range(camera.x, camera.right)):
                if y < 0 or self.height <= y or x < 0 or self.width <= x:
                    # put blank tile
                    continue
                tile = self.tile(x, y)

                if test:
                    blt.color("white")
                    blt.put(col, row, tile.char)

                if tile.explored:
                    color = "gray"
                    char = tile.char
                else:
                    color = "black"
                    char = Tiles.UNSEEN

                if tile.visible:
                    color = "white"
                    self.game_map.explore(tile.position)

                blt.puts(col, row, f"[color={color}]{char}[/color]")

    def can_see(self, entity: Entity, view: Rect) -> bool:
        if view.in_bounds(entity.position):
            if self.game_map.in_fov(entity.position):
                return True
        else:
            return False
