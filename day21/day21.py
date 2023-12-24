"""
Advent of Code Day 21
"""

import sys
from math import ceil, floor

from termcolor import colored


class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other: "Coord"):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coord"):
        return Coord(self.x - other.x, self.y - other.y)

    def __eq__(self, other: "Coord"):
        return self.x == other.x and self.y == other.y

    def __mul__(self, number: int):
        return Coord(self.x * number, self.y * number)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y)

    def distance(self, other: "Coord"):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def rotate(self, clockwise=True):
        x, y = self.y, self.x
        if clockwise:
            x *= -1
        else:
            y *= -1
        return Coord(x, y)


class Garden:
    garden_map: list[str]
    width: int
    height: int
    start: Coord
    patches: set[Coord]

    def __init__(
        self,
        garden_map: list[str],
    ):
        self.garden_map = garden_map.copy()
        self.width = len(garden_map)
        self.height = len(garden_map[0])
        for y, line in enumerate(garden_map):
            if (x := line.find("S")) >= 0:
                self.start = Coord(x, y)
        self.patches = set[Coord]()

    def __str__(self):
        drawing = ""

        min_corner, max_corner = self.get_patch_range()

        for y in range(min_corner.y, max_corner.y + 1):
            for x in range(min_corner.x, max_corner.x + 1):
                position = Coord(x, y)
                value = self.get(position)

                if value == "S" and (
                    position.x < 0
                    or position.x >= self.width
                    or position.y < 0
                    or position.y >= self.height
                ):
                    value = "."

                if value == "S":
                    drawing += colored(value, "white", "on_red")
                elif position in self.patches:
                    drawing += colored("x", "white", "on_green")
                else:
                    drawing += value

            if y < max_corner.y:
                drawing += "\n"

        return drawing

    def __repr__(self):
        return f"<garden_map [{self.width} x {self.height}]>"

    def get_patch_range(self):
        min_corner = self.start.copy()
        max_corner = self.start.copy()

        for patch in self.patches:
            min_corner.x = min(min_corner.x, patch.x)
            max_corner.x = max(max_corner.x, patch.x)
            min_corner.y = min(min_corner.y, patch.y)
            max_corner.y = max(max_corner.y, patch.y)

        min_corner = min_corner - self.constrain(min_corner)
        max_corner = (
            Coord(self.width - 1, self.height - 1)
            - self.constrain(max_corner)
            + max_corner
        )

        return (min_corner, max_corner)

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
        x, y = self.constrain(point)
        return self.garden_map[y][x]

    def find_patches(self, steps):
        self.patches.clear()
        self.patches.add(self.start)
        directions = [Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)]

        for _ in range(steps):
            new_patches = set[Coord]()

            for patch in self.patches:
                for direction in directions:
                    new_patch = patch + direction

                    if new_patch in new_patches:
                        continue

                    if self.get(new_patch) != "#":
                        new_patches.add(new_patch)

            self.patches = new_patches


def get_number_in_serial(base: list[int], place: int = None):
    if place is None:
        place = len(base)

    if place < len(base):
        return base[place]

    serials = [base]

    while any(number != 0 for number in serials[-1]):
        serials.append(
            [
                serials[-1][index] - serials[-1][index - 1]
                for index in range(1, len(serials[-1]))
            ]
        )

    try:
        layers = [serial[-1] for serial in serials]
    except IndexError:
        print("Series is not long enough to determine further values!")
        for serial in serials:
            print(serial)
        return None

    for _ in range(len(base), place + 1):
        for index in range(len(layers) - 2, -1, -1):
            layers[index] = layers[index] + layers[index + 1]

    return layers[0]


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        garden = Garden(file.read().splitlines())

        garden.find_patches(64)
        print(garden)
        print(f"In 64 steps {len(garden.patches)} plots can be reached")

        final_steps = 26501365
        base = 131
        modifier = 65
        series = 4
        steps_list = [base * index + modifier for index in range(series)]
        serials: list[int] = []
        fill = len(str(len(steps_list)))

        for index, steps in enumerate(steps_list):
            print(f"Step {index + 1:{fill}}/{len(steps_list):{fill}}", end="\r")
            garden.find_patches(steps)
            serials.append(len(garden.patches))

        patches = get_number_in_serial(serials, (final_steps - modifier) // base)

        print(
            f"In {final_steps} steps {patches if patches else '-'} plots can be reached"
        )


if __name__ == "__main__":
    main()
