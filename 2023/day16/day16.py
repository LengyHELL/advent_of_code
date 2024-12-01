"""
Advent of Code Day 16
"""

import sys
from termcolor import colored


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y)


class Beam:
    """
    Represents a light beam with its position and direction
    """

    position: Coord
    direction: Coord

    def __init__(self, position: Coord, direction: Coord):
        self.position = position
        self.direction = direction

    def rotate(self, clockwise=True):
        self.direction.x, self.direction.y = self.direction.y, self.direction.x
        if clockwise:
            self.direction.x *= -1
        else:
            self.direction.y *= -1

    def move(self):
        self.position += self.direction

    def reflect(self, mirror: str):
        if mirror == "\\":
            self.rotate(self.direction.y == 0)
        elif mirror == "/":
            self.rotate(self.direction.x == 0)

    def split(self, splitter: str):
        if (splitter == "-" and self.direction.y == 0) or (
            splitter == "|" and self.direction.x == 0
        ):
            return []

        right_split = Beam(self.position.copy(), self.direction.copy())
        left_split = Beam(self.position.copy(), self.direction.copy())

        right_split.rotate()
        left_split.rotate(False)

        right_split.move()
        left_split.move()

        return [right_split, left_split]


class Contraption:
    """
    Represents the contraption

    For more info refer to the day16 description
    """

    layout: list[str]
    beams: list[Beam]
    energized: set[Coord]
    width: int
    height: int

    def __init__(self, layout: list[str], beams: list[Beam] = None):
        self.layout = layout.copy()
        self.beams = beams.copy() if beams is not None else []
        self.energized = set[Coord]()
        self.width = len(layout)
        self.height = len(layout[0])

    def __str__(self):
        drawing = ""

        for y, line in enumerate(self.layout):
            for x, char in enumerate(line):
                if Coord(x, y) in self.energized:
                    drawing += colored(char, "black", "on_yellow")
                else:
                    drawing += char

            if y < (self.height - 1):
                drawing += "\n"

        return drawing

    def at(self, point: Coord):
        """
        Returns item found at `point`
        """
        return self.layout[point.y][point.x]

    def check_paths(self):
        for beam in self.beams:
            while (0 <= beam.position.x < self.width) and (
                0 <= beam.position.y < self.height
            ):
                if (item := self.at(beam.position)) != ".":
                    if item in "\\/":
                        beam.reflect(item)

                    elif beam.position not in self.energized:
                        new_beams = beam.split(item)

                        if len(new_beams) > 0:
                            self.beams.extend(new_beams)
                            self.energized.add(beam.position)
                            break
                    else:
                        break

                self.energized.add(beam.position)
                beam.move()


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().split("\n")
        most_energized = 0
        multiple = True  # set to False for part 1

        starting_beams = []

        if multiple:
            width = len(lines[0])
            height = len(lines)

            for y in range(height):
                starting_beams.append(Beam(Coord(0, y), Coord(1, 0)))
                starting_beams.append(Beam(Coord(width - 1, y), Coord(-1, 0)))

            for x in range(width):
                starting_beams.append(Beam(Coord(x, 0), Coord(0, 1)))
                starting_beams.append(Beam(Coord(x, height - 1), Coord(0, -1)))

        else:
            starting_beams.append(Beam(Coord(0, 0), Coord(1, 0)))

        for beam in starting_beams:
            contraption = Contraption(lines, [beam])
            contraption.check_paths()
            most_energized = max(most_energized, len(contraption.energized))

        print(f"The number of energized tiles is {most_energized}")


if __name__ == "__main__":
    main()
