import heapq
import itertools
from typing import List

import numpy as np

from map_objects.point import Point
from rect import Rect


class WeightedGrid(Rect):
    def __init__(self, x, y, width, height, blocked: np.array, weights: np.array = None):
        super(WeightedGrid, self).__init__(position=Point(x, y), width=width, height=height)
        self.blocked = blocked

        if weights is None:
            weights = np.ones_like(self.blocked, dtype=np.int)
        self.weights = weights

    def passable(self, point: Point):
        return not self.blocked[point.x, point.y]

    def neighbors(self, point: Point):
        for i, neighbor in enumerate(point.all_neighbors):
            if not self.in_bounds(neighbor):
                continue
            if self.passable(neighbor):
                if i % 2 == 1:
                    cost = round(1.4 * self.weights[neighbor.x, neighbor.y])
                else:
                    cost = self.weights[neighbor.x, neighbor.y]
                yield neighbor, cost


class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.counter = itertools.count()

    def empty(self) -> bool:
        return len(self.elements) == 0

    def put(self, point: Point, priority: int):
        count = next(self.counter)
        heapq.heappush(self.elements, (priority, count, point))

    def get(self) -> Point:
        return heapq.heappop(self.elements)[-1]


def heuristic(a: Point, b: Point):
    # x, y = a - b
    x = a.x - b.x
    y = a.y - b.y
    return abs(x) + abs(y)


def a_star_search(graph: WeightedGrid, start: Point, goal: Point):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: start}
    cost_so_far = {start: 0}
    # came_from[start] = None
    # cost_so_far[start] = 0
    current = Point(-1, -1)

    while not frontier.empty():
        last_point = current
        current: Point = frontier.get()

        if current == goal:
            came_from[current] = last_point
            print("breaking loop inside a_star search")
            break

        for neighbor, cost in graph.neighbors(current):
            # if not cost_so_far.get(current):
            #     print(f"cost={cost}, neighbor={neighbor}")
            #     print(f"current = {current}")
            #     for k, v in cost_so_far.items():
            #         print(f"{k} = {v}")
            new_cost = cost_so_far[current] + cost
            if cost_so_far.get(neighbor, False) is False or new_cost < cost_so_far.get(neighbor, 1000):
                cost_so_far[neighbor] = new_cost
                priority: int = new_cost + heuristic(goal, neighbor)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    return came_from, cost_so_far


def construct_path(came_from, start, goal) -> List[Point]:
    current = goal
    path = []
    print("going into path loop:")
    print(f"current = {current}")
    while current != start:
        path.append(current)
        print(f"current appended to path, path length is {len(path)}")
        current = came_from[current]
    return path


def find_path(start: Point, goal: Point, dungeon):
    blocked = dungeon.path_blocking
    blocked[start.x, start.y] = False
    graph = WeightedGrid(0, 0, dungeon.width, dungeon.height, blocked)
    came_from, cost_so_far = a_star_search(graph, start, goal)
    return construct_path(came_from, start, goal)
