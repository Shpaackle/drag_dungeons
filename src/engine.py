
# stdlib
import random
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

# pip installed
from bearlibterminal import terminal as blt

# app modules
from camera import Camera
from components import Fighter, Graphics, BasicMonster
from const import Tiles, MAP_SETTINGS, Layers, CAMERA_HEIGHT, CAMERA_WIDTH
from death_functions import kill_monster, kill_player
from entity import Entity, blocking_entities
from fov_functions import initialize_fov, update_fov
from game_states import GameStates
from handle_keys import handle_keys
from map_objects import Dungeon, Point, GameMap, Room, TileType
from render_functions import render_all, clear_all


class Engine:
    def __init__(self, random_seed=None):
        if random_seed is None:
            self.random_seed = datetime.now()
        else:
            self.random_seed = random_seed

        self.dungeon: Dungeon = None
        self.current_state: GameStates = None
        self.previous_state = None
        self.player: Entity = None
        self._entities: Dict[Point, List[Entity]] = defaultdict(list)
        self.camera: Camera = None
        self._fov_update: bool = False
        self.action = {}

    # TODO: refactor into generator
    @property
    def entities(self):
        yield self.player
        for entities in self._entities.values():
            for entity in entities:
                yield entity

    def initialize(self, test=False):
        self.current_state = GameStates.INITIALIZE
        random.seed(self.random_seed)
        print(self.random_seed)

        self.dungeon = Dungeon(MAP_SETTINGS)
        self.dungeon.build_dungeon()

        self.place_entities()

        self.camera = Camera(player=self.player)

        self.current_state = GameStates.PLAYER_TURN

        initialize_fov(self.game_map)

    @property
    def game_map(self) -> GameMap:
        return self.dungeon.game_map

    @property
    def fov_update(self) -> bool:
        return self._fov_update

    @fov_update.setter
    def fov_update(self, value: bool):
        self._fov_update = value

    def handle_input(self):
        key = None
        if blt.has_input():
            key = blt.read()

        action = handle_keys(key)

        if action.get("exit"):
            self.previous_state = self.current_state
            self.current_state = GameStates.EXIT

        self.action = action

    def update(self):
        current_state = self.current_state
        if current_state == GameStates.EXIT:
            return

        move = self.action.get("move")

        player_turn_results = []

        if move and current_state == GameStates.PLAYER_TURN:
            point = self.player.position + move
            if not self.dungeon.is_blocked(point):
                entities = self.dungeon.location_entities.get(point, [])

                target = None
                for entity in entities:
                    if entity.blocks:
                        target = entity
                if target:
                    # print(f"You kick the {target} in the shins, much to its annoyance!")
                    attack_results = self.player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    self.player.move(move)
                    self.camera.recenter(self.player.position)

                self._fov_update = True

                self.previous_state = current_state
                self.current_state = GameStates.ENEMY_TURN

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity: Entity = player_turn_result.get("dead")

            if message:
                print(message)

            if dead_entity:
                if dead_entity == self.player:
                    message, game_state = kill_player(dead_entity)
                else:
                    # self.dungeon.location_entities.pop(dead_entity.position)
                    message = kill_monster(dead_entity)

                print(message)

        if current_state == GameStates.ENEMY_TURN:
            # entity: Entity
            for entity in iter(self.entities):
                if entity.ai:
                    if self.dungeon.can_see(entity=entity, view=self.camera):
                        enemy_turn_results = entity.ai.take_turn(target=self.player, dungeon=self.dungeon, entity_locations=self.entity_locations)

                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get("message")
                            dead_entity = enemy_turn_result.get("dead")

                            if message:
                                print(message)
                            if dead_entity:
                                if dead_entity == self.player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)
                                    # self.dungeon.location_entities.pop(dead_entity.position)
                                    game_state = None

                                print(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    self.previous_state = current_state
                                    self.current_state = game_state
                                    break
                        if self.current_state == GameStates.PLAYER_DEAD:
                            break
                # print(f"The {entity} ponders the meaning of its existence.")
            else:
                self.previous_state = current_state
                self.current_state = GameStates.PLAYER_TURN

        if self.fov_update:
            update_fov(self.game_map, self.player.position)
            # game_map = self.dungeon.maps(self.camera.position, self.camera.width, self.camera.height)
            # self.game_map = game_map

    def render(self):
        # x = max(self.camera.x, 0)
        # y = max(self.camera.y, 0)
        # x2 = min(x1 + self.camera.width, self.dungeon.width - 1)
        # y2 = min(y1 + self.camera.height, self.dungeon.height - 1)
        # tile_map = self.dungeon.tile_map(
        #     x1=x,
        #     y1=y,
        #     width=min(self.camera.width, self.dungeon.width),
        #     height=min(self.camera.height, self.dungeon.height))

        render_all(
            player=self.player,
            entities=self.entities,
            fov_update=self.fov_update,
            camera=self.camera,
            dungeon=self.dungeon
        )
        blt.refresh()
        clear_all(self.entities)

    @property
    def entity_locations(self):
        return self._entities

    def place_entities(self):
        max_monsters_per_room = MAP_SETTINGS["max_monsters_per_room"]

        rooms = self.dungeon.rooms
        starting_room: Room = random.choice(rooms)

        player = Entity(
            name="Player",
            position=starting_room.top_left,
            char=Tiles.PLAYER,
            color="white",
            blocks=True,
            fighter=Fighter(hp=100, defense=8, power=10),
            graphics=Graphics(),
        )
        self.player = player

        entities = {}

        for room in iter(rooms):
            if room == starting_room:
                continue

            for i in range(random.randrange(max_monsters_per_room)):
                x = random.randrange(room.left, room.right)
                y = random.randrange(room.top, room.bottom)
                point = Point(x, y)

                if not self.entity_locations.get(point):
                    if random.randrange(100) < 80:
                        monster = Entity(
                            name="goblin",
                            position=point,
                            char=Tiles.GOBLIN,
                            blocks=True,
                            fighter=Fighter(hp=16, defense=1, power=4),
                            ai=BasicMonster(),
                            graphics=Graphics()
                        )
                    else:
                        monster = Entity(
                            name="orc",
                            position=point,
                            char=Tiles.ORC,
                            blocks=True,
                            fighter=Fighter(hp=16, defense=1, power=4),
                            ai=BasicMonster(),
                            graphics=Graphics()
                        )

                    self._entities[point].append(monster)
                    self.dungeon.place_entity(monster)

    def entities_at_location(self, point: Point) -> list:
        entities = []
        for entity in self.dungeon.entities:
            if entity.position == point:
                entities.append(entity)
        return entities


def main():
    # engine = Engine(random_seed="TEST_MAP")
    engine = Engine()
    engine.initialize()

    engine.fov_update = True
    engine.update()
    engine.render()

    while not engine.current_state == GameStates.EXIT:
        engine.handle_input()
        engine.update()
        engine.render()


if __name__ == "__main__":
    blt.open()
    blt.composition(True)
    blt.set(f"window: size=31x21, cellsize=auto, title='Drag Dungeons'")
    blt.set("font: data/mplus-1p-regular.ttf, size=32x32")
    blt.set("interface font: data/mplus-1p-regular.ttf, size=8x16")
    blt.set("0xE000: data/ProjectUtumno_full.png, size=32x32")
    # logger.add(
    #     "logs/build_maze_{time}.log",
    #     level="ERROR",
    #     format="{time:HH:mm:ss.SSS} {message}",
    # )
    main()
    blt.close()
