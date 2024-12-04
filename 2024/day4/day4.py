"""
Advent of Code Day 4
"""

import sys


class Coord:
    """
    Represents a 2d coordinate
    """

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y)


class Grid:
    """
    Represents the grid
    """

    layout: list[str]
    width: int
    height: int

    def __init__(self, layout: list[str]):
        self.layout = layout.copy()
        self.width = len(layout)
        self.height = len(layout[0])

    def __str__(self):
        drawing = ""

        for y, line in enumerate(self.layout):
            for char in line:
                drawing += char

            if y < (self.height - 1):
                drawing += "\n"

        return drawing

    def at(self, point: Coord):
        """
        Returns item found at `point`
        """
        return self.layout[point.y][point.x]

    def in_bounds(self, point: Coord):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def find_word(self, word: str):
        matches = 0
        directions = [
            Coord(0, 1),
            Coord(1, 1),
            Coord(1, 0),
            Coord(1, -1),
            Coord(0, -1),
            Coord(-1, -1),
            Coord(-1, 0),
            Coord(-1, 1),
        ]

        for l, line in enumerate(self.layout):
            for i, _ in enumerate(line):
                for d in directions:
                    match = True
                    location = Coord(l, i)

                    for char in word:
                        if not self.in_bounds(location) or char != self.at(location):
                            match = False
                            break
                        location += d

                    if match:
                        matches += 1

        return matches

    def find_x_mas(self):
        x_mas_matches = 0
        directions = [
            Coord(1, 1),
            Coord(1, -1),
            Coord(-1, -1),
            Coord(-1, 1),
        ]

        for l, line in enumerate(self.layout):
            for i, _ in enumerate(line):
                matches = 0

                for d in directions:
                    match = True
                    location = Coord(l, i) - d

                    for char in "MAS":
                        if not self.in_bounds(location) or char != self.at(location):
                            match = False
                            break
                        location += d

                    if match:
                        matches += 1

                if matches >= 2:
                    x_mas_matches += 1

        return x_mas_matches


with open(sys.argv[1], encoding="utf-8") as file:
    grid = Grid(file.read().split("\n"))
    occurrances = grid.find_word("XMAS")
    x_mases = grid.find_x_mas()

    print(f"XMAS appears {occurrances} times.")
    print(f"X-MAX appears {x_mases} times.")
