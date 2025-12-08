"""
Advent of Code 2025 Day 7
"""

import sys
from typing import List, Set
from functools import cache

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid

class Manifold(Grid):
    start: Coord
    beam: Set[Coord]
    splits: int
    timelines: int

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)
        self.start = self.find_start()
        self.beam = set()
        self.splits = 0
        self.timelines = 0

    def __str__(self):
        drawing = ""

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if value == "S":
                    drawing += colored(value, "green")
                elif value == "^":
                    drawing += colored(value, "red")
                elif position in self.beam:
                    drawing += colored("|", "blue")
                else:
                    drawing += value

            if y < self.height:
                drawing += "\n"

        return drawing

    def find_start(self) -> Coord:
        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                if self.get(position) == "S":
                    return position

    def simulate_beam(self):
        queue = [self.start]
        self.beam = set()
        self.splits = 0

        while len(queue) > 0:
            current = queue.pop(0)
            self.beam.add(current)
            checking = current + Coord(0, 1)

            if self.get(checking) == "^":
                self.splits += 1
                splits = [Coord(-1, 1), Coord(1, 1)]
                for s in splits:
                    new = current + s
                    new_value = self.get(new)
                    if new_value is not None and new not in queue:
                        queue.append(new)
            else:
                checking_value = self.get(checking)
                if checking_value is not None and checking not in queue:
                    queue.append(checking)

    def calculate_timelines(self):
        self.timelines = get_timeline(self, self.start)

@cache
def get_timeline(manifold: Manifold, pos: Coord) -> int:
    timelines = 0

    while True:
        pos += Coord(0, 1)
        if manifold.get(pos) == "^":
            timelines += get_timeline(manifold, pos + Coord(-1, 0))
            timelines += get_timeline(manifold, pos + Coord(1, 0))
            break
        elif manifold.get(pos) is None:
            timelines += 1
            break

    return timelines


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        manifold = Manifold(file.read().splitlines())

        manifold.simulate_beam()
        manifold.calculate_timelines()
        manifold.print()

        print(
            f"There are {manifold.splits} splits, with a total of {manifold.timelines} timelines."
        )

if __name__ == "__main__":
    main()
