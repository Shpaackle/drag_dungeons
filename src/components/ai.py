class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, dungeon, entity_locations: dict):
        results = []

        monster = self.owner
        if monster.position.distance(target.position) >= 2:
            old_position = monster.position
            monster.move_a_star(target, dungeon=dungeon, entity_locations=entity_locations)
            # monster.move_towards(target.position, entity_locations=entity_locations, game_map=dungeon.game_map, dungeon=dungeon)
            # dungeon.move_entity(entity=monster, old_position=old_position, new_position=monster.position)
        elif target.fighter.hp > 0:
            # print(f"The {monster} insults you! Your ego is damaged!")
            # monster.fighter.attack(target)
            attack_results = monster.fighter.attack(target)
            results.extend(attack_results)

        return results
