class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, dungeon, entity_locations):
        print(f"The {self.owner} wonders when it will get to move.")
        monster = self.owner
        if monster.position.distance(target.position) >= 2:
            monster.move_towards(target.position, entity_locations=entity_locations, game_map=dungeon.game_map)
        elif target.fighter.hp > 0:
            print(f"The {monster} insults you! Your ego is damaged!")
        # monster = self.owner
        # if game_map.in_fov(monster.position):
        #     if monster.position.distance(target.position) >= 2:
        #         monster.move_towards(target.position, game_map, entities)
        #
        #     elif target.fighter.hp > 0:
        #         print(f"The {monster} insults you! Your ego is damaged!")
