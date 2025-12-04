"""
Advent of Code 2025 Day 4
"""

import sys
from typing import List, Set

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class Warehouse(Grid):
    accessible: Set[Coord]
    removed: int

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)
        self.accessible = set()
        self.removed = 0

    def __str__(self):
        drawing = ""

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if position in self.accessible:
                    drawing += colored(value, "white", "on_green")
                else:
                    drawing += value

            if y < self.height:
                drawing += "\n"

        return drawing
    
    def get_surrounding(self, position: Coord) -> int:
        items = 0

        for y in range(-1, 2):
            for x in range(-1, 2):
                if Coord(x, y) == Coord(0, 0):
                    continue

                check = position + Coord(x, y)
                value = self.get(check)

                if value == "@":
                    items += 1
        
        return items

    def find_accessible(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if value == "@" and self.get_surrounding(position) < 4:
                    self.accessible.add(position)
    
    def remove_rolls(self):
        while True:
            self.accessible.clear()
            self.find_accessible()

            if (size := len(self.accessible)) > 0:
                self.removed += size
                print(f"Removing {size} rolls...")
            else:
                break

            for roll in self.accessible:
                self.set(roll, ".")


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        warehouse = Warehouse(file.read().splitlines())

        warehouse.find_accessible()
        warehouse.print()
        print(f"There are {len(warehouse.accessible)} accessible rolls.")

        warehouse.remove_rolls()
        warehouse.print()
        print(f"There are {warehouse.removed} rolls that can be removed.")

if __name__ == "__main__":
    main()
