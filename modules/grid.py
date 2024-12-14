from math import ceil, floor
from typing import List

from modules.coord import Coord


class Grid:
    grid: List[str]
    width: int
    height: int

    def __init__(
        self,
        grid: List[str],
    ):
        self.grid = grid.copy()
        self.height = len(grid)
        self.width = len(grid[0])

    def __str__(self):
        drawing = ""

        for y in range(self.height):
            for x in range(self.width):
                drawing += self.draw_cell(Coord(x, y))

            if y < self.height:
                drawing += "\n"

        return drawing

    def draw_cell(self, position):
        return self.get(position)

    def print(self):
        print(*str(self).split("\n"), sep="\n")

    def __repr__(self):
        return f"<grid [{self.width} x {self.height}]>"

    def in_bounds(self, point: Coord):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

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
        if not self.in_bounds(point):
            return None
        return self.grid[point.y][point.x]

    def set(self, point: Coord, value: str):
        if self.in_bounds(point):
            row = self.grid[point.y]
            self.grid[point.y] = row[: point.x] + value + row[point.x + 1 :]
