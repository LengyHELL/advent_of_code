"""
Advent of Code Day 20
"""

import sys
from typing import List, Set, Dict
from functools import reduce

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class Node:
    pos: Coord
    prev: "Node"
    dist: int

    def __init__(self, pos: Coord, prev: "Node", dist: int):
        self.pos = pos
        self.prev = prev
        self.dist = dist


class Racetrack(Grid):
    start: Coord
    end: Coord
    route: List[Coord]
    shortcuts: Dict[int, int]
    shortcut_count: int
    highlighted: List[Coord]

    def __init__(self, grid: List[str]):
        Grid.__init__(self, grid)

        self.__find_items()
        self.route = []
        self.shortcuts = dict()
        self.shortcut_count = 0
        self.highlighted = []

    def __str__(self):
        drawing = [list(line) for line in self.grid]

        colorings = [
            *[(pos, "white", "on_blue", None) for pos in self.route],
            (self.start, "white", "on_green", None),
            (self.end, "white", "on_red", None),
            *[(pos, "white", "on_yellow", None) for pos in self.highlighted],
        ]

        for pos, color, on_color, value in colorings:
            if value is None:
                value = self.get(pos)
            drawing[pos.y][pos.x] = colored(value, color, on_color)

        return "\n".join(["".join(line) for line in drawing])

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

    def find_route(self):
        queue = [Node(self.start, None, 0)]
        checked: Set[Coord] = set()
        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]

        while len(queue) > 0:
            queue.sort(key=lambda q: q.dist)
            current = queue.pop(0)

            if current.pos == self.end:
                self.route = []

                while True:
                    self.route.insert(0, current.pos)
                    if current.prev is None or current.pos == self.start:
                        break
                    current = current.prev
                return

            checked.add(current.pos)

            for d in directions:
                new_position = current.pos + d

                if (
                    self.in_bounds(new_position)
                    and self.get(new_position) != "#"
                    and new_position not in checked
                    and new_position not in [q.pos for q in queue]
                ):
                    queue.append(Node(new_position, current, current.dist + 1))

    def find_shortcuts(self, limit: int, save_limit: int):
        area: List[Coord] = []

        for y in range(-limit, limit + 1):
            for x in range(-limit, limit + 1):
                position = Coord(x, y)
                dist = position.distance()

                if dist <= limit and dist != 0:
                    area.append(position)

        route_length = len(self.route)
        self.shortcuts.clear()

        for c, current in enumerate(self.route):
            print(f"{c}/{len(self.route)}", end="\r")
            route_set = set(self.route[c + 1 :])

            for a in area:
                new_position = current + a

                if new_position in route_set:
                    index = self.route.index(new_position)
                    save = route_length - (c + a.distance() + (route_length - index))

                    if save >= save_limit:
                        if save in self.shortcuts:
                            self.shortcuts[save] += 1
                        else:
                            self.shortcuts[save] = 1

        self.shortcut_count = reduce(
            lambda sum, item: sum + item, self.shortcuts.values(), 0
        )

    def print_shortcut_info(self):
        for save, count in sorted(self.shortcuts.items(), key=lambda x: x[0]):
            print(f"There are {count} cheats that save {save} picoseconds.")


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        track = Racetrack(file.read().splitlines())
        track.find_route()
        track.print()
        pairs = [(2, 100), (20, 100)]

        for limit, save_limit in pairs:
            track.find_shortcuts(limit, save_limit)
            # track.print_shortcut_info()
            print(
                f"There are {track.shortcut_count} cheats that would save at least {save_limit} picoseconds if the cheats can last {limit} picoseconds."
            )


if __name__ == "__main__":
    main()
