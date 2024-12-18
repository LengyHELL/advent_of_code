"""
Advent of Code Day 18
"""

import sys
import re
from typing import List
from math import ceil

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


class MemoryGrid(Grid):
    bytes: List[Coord]
    steps: int
    start: Coord
    end: Coord
    highlighted: Coord
    route: List[Coord]

    def __init__(self, data: str):
        width, height = self.__to_bytes(data)
        grid = ["." * width] * height
        super().__init__(grid)

        self.steps = 0
        self.start = Coord(0, 0)
        self.end = Coord(self.width - 1, self.height - 1)
        self.highlighted = None
        self.route = []

    def __to_bytes(self, data: str):
        self.bytes = []

        br = Coord(0, 0)

        for line in data.splitlines():
            x_str, y_str = re.match(r"(\d+),(\d+)", line).groups()
            byte = Coord(int(x_str), int(y_str))

            self.bytes.append(byte)

            if byte.x > br.x:
                br.x = byte.x
            if byte.y > br.y:
                br.y = byte.y

        return br + Coord(1, 1)

    def draw_cell(self, position):
        value = self.get(position)

        if self.highlighted is not None and self.highlighted == position:
            return colored(value, None, "on_yellow")
        elif position == self.start:
            return colored(value, None, "on_green")
        elif position == self.end:
            return colored(value, None, "on_red")
        elif position in self.bytes[: self.steps]:
            return "#"
        elif position in self.route:
            return colored(value, None, "on_blue")
        else:
            return value

    def find_route(self):
        queue = [Node(self.start, None, 0)]
        checked: List[Node] = []
        self.route = []

        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]

        while len(queue) > 0:
            current = queue.pop(0)

            if current.pos == self.end:
                while True:
                    if current.prev is None or current.pos == self.start:
                        break
                    self.route.insert(0, current.pos)
                    current = current.prev
                return True

            checked.append(current)

            for d in directions:
                new_position = current.pos + d

                if (
                    self.in_bounds(new_position)
                    and new_position not in self.bytes[: self.steps]
                    and new_position not in [q.pos for q in queue]
                    and new_position not in [c.pos for c in checked]
                ):
                    queue.append(Node(new_position, current, current.dist + 1))

        self.highlighted = self.bytes[self.steps - 1]
        return False


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        grid = MemoryGrid(file.read())
        start = 1024
        end = len(grid.bytes) - 1
        grid.steps = start
        first = True
        while True:
            found = grid.find_route()
            if first:
                grid.print()
                print(f"The minimum number of steps needed is {len(grid.route)}.")
                first = False

            if found:
                start = grid.steps
            else:
                end = grid.steps

            if end - 1 == start:
                break

            grid.steps = start + ceil((end - start) / 2)

        print()
        grid.print()
        print(
            f"The first byte that will prevent the exit from being reachable is {grid.highlighted}."
        )


if __name__ == "__main__":
    main()
