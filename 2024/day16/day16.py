"""
Advent of Code Day 16
"""

import sys
from typing import List, Set, Tuple
from math import inf

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class Node:
    pos: Coord
    prev: "Node"
    dist: int

    def __init__(self, pos: Coord, prev: "Node", dist: int = inf):
        self.pos = pos
        self.prev = prev
        self.dist = dist


class Maze(Grid):
    start: Coord
    end: Coord
    graph: List[Node]
    score: int
    path: List[Coord]
    highlighted: Coord
    positions: int

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)

        self.__find_items()
        self.graph = []
        self.score = 0
        self.path = []
        self.highlighted = None
        self.positions = 0

    def draw_cell(self, position):
        value = self.get(position)

        if self.highlighted is not None and position == self.highlighted:
            return colored(value, "white", "on_yellow")
        elif position == self.start:
            return colored(value, "white", "on_green")
        elif position == self.end:
            return colored(value, "white", "on_red")
        elif position in self.path:
            return colored(value, "white", "on_blue")
        else:
            return value

    def __find_items(self):
        self.start = None
        self.end = None

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if value == "S":
                    self.start = position
                elif value == "E":
                    self.end = position

    def create_graph(self):
        self.graph = []
        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]
        queue = [Node(self.start, Node(self.start - Coord(1, 0), None), 0)]

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)
                if value == "." or value == "E":
                    queue.append(Node(position, None))

        while len(queue) > 0:
            queue.sort(key=lambda node: node.dist)
            current = queue.pop(0)
            self.graph.append(current)
            direction = current.pos - current.prev.pos

            for d in directions:
                new_position = current.pos + d
                neighbors = [q for q in queue if q.pos == new_position]

                if len(neighbors) <= 0:
                    continue

                neighbor = neighbors[0]
                new_dist = current.dist + 1

                if direction != d:
                    new_dist += 1000

                if new_dist < neighbor.dist:
                    neighbor.dist = new_dist
                    neighbor.prev = current

    def find_shortest_path(self):
        try:
            current = [g for g in self.graph if g.pos == self.end][0]
        except IndexError:
            return
        self.path = []
        self.score = current.dist

        while True:
            if current.prev is None or current.pos == self.start:
                break
            self.path.insert(0, current.pos)
            current = current.prev

    def find_shortest_path_positions(self):
        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]
        queue: List[Tuple[Coord, Node]] = [
            (None, g) for g in self.graph if g.pos == self.end
        ]
        checked: Set[Node] = set()

        while True:
            direction, current = queue.pop(0)
            if current.pos == self.start:
                break

            checked.add(current)

            neighbors: List[Tuple[int, Tuple[Coord, Node]]] = []
            for d in directions:
                position = current.pos + d
                try:
                    neighbor = [node for node in self.graph if node.pos == position][0]
                    score = neighbor.dist
                    if direction is None or direction == d:
                        score -= 1000

                    neighbors.append((score, (d, neighbor)))
                except IndexError:
                    continue

            neighbors.sort(key=lambda n: n[0])
            to_queue = [
                n[1]
                for n in neighbors
                if n[0] == neighbors[0][0] and n[1] not in checked and n[1] not in queue
            ]
            queue.extend(to_queue)

        self.positions = len(checked) + 1


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        maze = Maze(file.read().splitlines())
        maze.create_graph()
        maze.find_shortest_path()
        maze.print()
        print(f"The lowest score a Reindeer could possibly get is {maze.score}.")

        maze.find_shortest_path_positions()
        print(f"{maze.positions} tiles are part of at least one of the best paths.")


if __name__ == "__main__":
    main()
