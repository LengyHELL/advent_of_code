"""
Advent of Code Day 6
"""

import sys
from math import ceil, floor
from typing import List, Tuple, Set

from termcolor import colored

from modules.coord import Coord


class Grid:
    grid: List[str]
    width: int
    height: int
    start: Coord
    route: Set[Tuple[Coord, Coord]]
    obstructions: List[Coord]

    def __init__(
        self,
        grid: List[str],
    ):
        self.grid = grid.copy()
        self.width = len(grid)
        self.height = len(grid[0])
        for y, line in enumerate(grid):
            if (x := line.find("^")) >= 0:
                self.start = Coord(x, y)
        self.route = []
        self.obstructions = []

    def __str__(self):
        drawing = ""
        route_positions = [position[0] for position in self.route]

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if position in self.obstructions:
                    drawing += colored(value, "white", "on_blue")
                elif value == "^":
                    drawing += colored(value, "white", "on_green")
                elif value == "#":
                    drawing += colored(value, "white", "on_red")
                elif position in route_positions:
                    drawing += colored(value, "white", "on_yellow")
                else:
                    drawing += value

            if y < self.height:
                drawing += "\n"

        return drawing

    def print(self):
        print(*str(self).split("\n"), sep="\n")

    def __repr__(self):
        return f"<grid [{self.width} x {self.height}]>"

    def constrain(self, point: Coord):
        x, y = point

        if x < 0:
            x += self.width * ceil(abs(x) / self.width)
        elif x >= self.width:
            x -= self.width * floor(abs(x) / self.width)

        if y < 0:
            y += self.height * ceil(abs(y) / self.height)
        elif y >= self.height:
            y -= self.height * floor(abs(y) / self.height)

        return Coord(x, y)

    def get(self, point: Coord):
        if point != self.constrain(point):
            return None
        return self.grid[point.y][point.x]

    def set(self, point: Coord, value: str):
        row = self.grid[point.y]
        self.grid[point.y] = row[: point.x] + value + row[point.x + 1 :]

    def find_route(self):
        self.route = set()
        direction = Coord(0, -1)
        position = self.start.copy()

        while position == self.constrain(position):
            self.route.add(((position, direction)))

            while self.get(position + direction) == "#":
                direction = direction.rotate()

            position += direction

            if (position, direction) in self.route:
                return True

        return False

    def get_visited_positions(self):
        return len(dict.fromkeys([position[0] for position in self.route]))

    def find_obstructions(self):
        stored_route = self.route
        route = dict.fromkeys(stored_route)
        route_dict = dict.fromkeys(route)
        fill = len(str(len(route_dict))) + 1

        for index, (position, _) in enumerate(route_dict):
            temp = self.get(position)
            self.set(position, "#")

            if self.find_route() and position not in self.obstructions:
                self.obstructions.append(position)

            self.set(position, temp)
            print(f"{index:{fill}} / {len(route_dict):{fill}}", end="\r")

        self.route = stored_route

    def get_obstructions(self):
        return len(self.obstructions)


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        guard_map = Grid(file.read().splitlines())

        guard_map.find_route()
        guard_map.print()
        print(f"The length of the route is {guard_map.get_visited_positions()}")

        guard_map.find_obstructions()
        guard_map.print()
        print(f"There are {guard_map.get_obstructions()} obstructable positions.")


if __name__ == "__main__":
    main()
