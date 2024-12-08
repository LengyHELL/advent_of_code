"""
Advent of Code Day 4
"""

import sys
from modules.coord import Coord
from modules.grid import Grid


class WordGrid(Grid):
    def __init__(self, grid: list[str]):
        Grid.__init__(self, grid)

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

        for l, line in enumerate(self.grid):
            for i, _ in enumerate(line):
                for d in directions:
                    match = True
                    location = Coord(l, i)

                    for char in word:
                        if not self.in_bounds(location) or char != self.get(location):
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

        for l, line in enumerate(self.grid):
            for i, _ in enumerate(line):
                matches = 0

                for d in directions:
                    match = True
                    location = Coord(l, i) - d

                    for char in "MAS":
                        if not self.in_bounds(location) or char != self.get(location):
                            match = False
                            break
                        location += d

                    if match:
                        matches += 1

                if matches >= 2:
                    x_mas_matches += 1

        return x_mas_matches


with open(sys.argv[1], encoding="utf-8") as file:
    grid = WordGrid(file.read().split("\n"))

    occurrances = grid.find_word("XMAS")
    print(f"XMAS appears {occurrances} times.")

    x_mases = grid.find_x_mas()
    print(f"X-MAX appears {x_mases} times.")
