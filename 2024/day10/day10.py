"""
Advent of Code Day 10
"""

import sys
from typing import List, Set

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class TrailMap(Grid):
    starts: List[Coord]

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)

        self.find_starts()

    def draw_cell(self, position):
        value = self.get(position)

        if position in self.starts:
            return colored(value, "white", "on_blue")
        else:
            return value

    def find_starts(self):
        self.starts = []

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)

                if self.get(position) == "0":
                    self.starts.append(position)

    def find_route(self, position, rating=False):
        found_routes = 0
        queue = [position]
        checked: Set[Coord] = set()
        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]

        while len(queue) > 0:
            current = queue.pop(0)
            checked.add(current)

            if self.get(current) == "9":
                found_routes += 1
                continue

            for direction in directions:
                position = current + direction

                if (
                    self.in_bounds(position)
                    and int(self.get(position)) == int(self.get(current)) + 1
                    and position not in checked
                    and (rating or position not in queue)
                ):
                    queue.append(position)

        return found_routes

    def get_trails_score(self, rating=False):
        total_score = 0

        for start in self.starts:
            routes = self.find_route(start, rating)
            total_score += routes

        return total_score


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        trail_map = TrailMap(file.read().splitlines())
        trail_map.print()
        print(f"The sum of the trailhead scores is {trail_map.get_trails_score()}.")
        print(
            f"The sum of the trailhead ratings is {trail_map.get_trails_score(True)}."
        )


if __name__ == "__main__":
    main()
