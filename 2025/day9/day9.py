"""
Advent of Code 2025 Day 9
"""

import sys
from typing import List, Tuple

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid

class Theater(Grid):
    red_tiles: List[Coord]
    biggest: Tuple[Coord, Coord]
    area: int

    def __init__(
        self,
        data: str
    ):
        Grid.__init__(self, self.__process_data(data))
        self.biggest = (Coord(0, 0), Coord(0, 0))
        self.area = 0

    def __str__(self):
        drawing = ""

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if position in self.biggest:
                    drawing += colored("O", "red")
                elif self.__in_biggest(position):
                    drawing += "O"
                elif position in self.red_tiles:
                    drawing += colored("#", "red")
                elif self.__in_area(position):
                    drawing += colored("X", "green")
                else:
                    drawing += value

            if y < self.height:
                drawing += "\n"

        return drawing


    def __process_data(self, data: str) -> List[str]:
        lines = data.splitlines()
        self.red_tiles = []

        for line in lines:
            x, y = map(int, line.split(","))
            self.red_tiles.append(Coord(x, y))

        min_x = min(self.red_tiles, key=lambda t: t.x).x
        min_y = min(self.red_tiles, key=lambda t: t.y).y
        max_x = max(self.red_tiles, key=lambda t: t.x).x + 1
        max_y = max(self.red_tiles, key=lambda t: t.y).y + 1

        return ["." * (max_x + min_x) for _ in range(max_y + min_y)]

    def __calculate_area(self, c1: Coord, c2: Coord) -> int:
        n = (c1 - c2).abs() + Coord(1, 1)
        return n.x * n.y

    def __in_biggest(self, position: Coord) -> bool:
        r1, r2 = self.biggest
        tl = Coord(min(r1.x, r2.x), min(r1.y, r2.y))
        br = Coord(max(r1.x, r2.x), max(r1.y, r2.y))
        return tl <= position <= br

    def __in_area(self, position: Coord) -> bool:
        size = len(self.red_tiles)
        x, y = position
        inside = False

        p1 = self.red_tiles[0]

        for i in range(1, size + 1):
            p2 = self.red_tiles[i % size]

            if y == p1.y == p2.y and min(p1.x, p2.x) <= x <= max(p1.x, p2.x):
                return True
            elif min(p1.y, p2.y) < y <= max(p1.y, p2.y):
                if x == p1.x == p2.x:
                    return True
                elif x <= max(p1.x, p2.x):
                    inside = not inside

            p1 = p2

        return inside

    def __check_area(self, r1: Coord, r2: Coord):
        tl = Coord(min(r1.x, r2.x), min(r1.y, r2.y))
        br = Coord(max(r1.x, r2.x), max(r1.y, r2.y))
        edges = [tl, Coord(tl.x, br.y), br, Coord(br.x, tl.y)]

        size = len(edges)
        p1 = edges[0]

        for i in range(1, size + 1):
            p2 = edges[i % size]
            d = p2 - p1
            d = Coord(
                d.x / abs(d.x) if d.x != 0 else 0,
                d.y / abs(d.y) if d.y != 0 else 0
            )

            current = p1
            while True:
                if current == p2:
                    break
                if not self.__in_area(current):
                    return True
                current += d

            p1 = p2

        return False

    def find_biggest(self, check_area = False):
        self.biggest = (Coord(0, 0), Coord(0, 0))
        self.area = 0

        for i, r1 in enumerate(self.red_tiles):
            print(
                f"Tiles: {i + 1:<{len(str(len(self.red_tiles)))}} / {len(self.red_tiles)}", end="\r"
            )

            for r2 in self.red_tiles[i + 1:]:
                if check_area and self.__check_area(r1, r2):
                    continue

                if (a := self.__calculate_area(r1, r2)) > self.area:
                    self.biggest = (r1, r2)
                    self.area = a


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        theater = Theater(file.read())
        enable_print = theater.width <= 200 and theater.height <= 200

        if enable_print:
            theater.print()

        theater.find_biggest()

        if enable_print:
            theater.print()

        print(f"The largest area is {theater.area}.")

        theater.find_biggest(True)

        if enable_print:
            theater.print()

        print(f"The largest area with green tiles is {theater.area}.")
        # 4655183296 too high

if __name__ == "__main__":
    main()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
