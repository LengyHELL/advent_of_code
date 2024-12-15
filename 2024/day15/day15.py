"""
Advent of Code Day 15
"""

import sys
from typing import List, Union

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class Box:
    tl: Coord
    br: Coord

    def __init__(self, tl: Coord, br: Coord):
        self.tl = tl
        self.br = br

    def __iter__(self):
        return iter((self.tl, self.br))

    def __contains__(self, item: Union["Box", Coord]):
        if isinstance(item, Box):
            return (
                item.tl.x <= self.br.x
                and self.tl.x <= item.br.x
                and item.tl.y <= self.br.y
                and self.tl.y <= item.br.y
            )
        if isinstance(item, Coord):
            return self.tl <= item <= self.br

    def __eq__(self, other: "Box"):
        return self.tl == other.tl and self.br == other.br

    def __add__(self, other: Coord):
        return Box(self.tl + other, self.br + other)

    def __body(self):
        if self.tl == self.br:
            return ["O"]
        elif self.tl.y == self.br.y:
            diff = self.br.x - self.tl.x - 2
            return ["[" + diff * "O" + "]"]
        else:
            width, height = self.br - self.tl + Coord(1, 1)
            return ["O" * width] * height

    def value(self, at: Coord):
        x, y = at - self.tl
        return self.__body()[y][x]


class Warehouse(Grid):
    start: Coord
    robot_position: Coord
    boxes: List[Box]
    moves: List[Coord]

    def __init__(self, grid: List[str], moves: str):
        Grid.__init__(self, grid)

        self.__find_items()
        self.__get_moves(moves)
        self.robot_position = self.start.copy()

    def __str__(self):
        drawing = [list(line) for line in self.grid]

        drawing[self.robot_position.y][self.robot_position.x] = colored(
            "@", None, "on_yellow"
        )

        for box in self.boxes:
            for y in range(box.tl.y, box.br.y + 1):
                for x in range(box.tl.x, box.br.x + 1):
                    drawing[y][x] = colored(box.value(Coord(x, y)), None, "on_blue")

        return "\n".join(["".join(line) for line in drawing])

    def __find_items(self):
        self.start = None
        self.boxes = []

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if value == "O":
                    self.boxes.append(Box(position, position))
                    self.set(position, ".")
                elif value == "[":
                    self.boxes.append(Box(position, position + Coord(1, 0)))
                    self.set(position, ".")
                    self.set(position + Coord(1, 0), ".")
                elif value == "@":
                    self.start = position
                    self.set(position, ".")

    def __get_moves(self, moves: str):
        self.moves = []

        for move in moves:
            if move == ">":
                self.moves.append(Coord(1, 0))
            elif move == "v":
                self.moves.append(Coord(0, 1))
            elif move == "<":
                self.moves.append(Coord(-1, 0))
            elif move == "^":
                self.moves.append(Coord(0, -1))

    def __check_boxes(self, index: int, direction: Coord):
        boxes_to_move: List[int] = []
        new_box = self.boxes[index] + direction

        collisions = [new_box in box and i != index for i, box in enumerate(self.boxes)]

        if collisions.count(True) > 0:
            for collision_index, collision in enumerate(collisions):
                if not collision:
                    continue

                to_move = self.__check_boxes(collision_index, direction)

                if len(to_move) <= 0:
                    return []

                boxes_to_move.extend(to_move)

        if all([self.in_bounds(part) and self.get(part) != "#" for part in new_box]):
            boxes_to_move.append(index)
            return boxes_to_move

        return []

    def simulate_moves(self):
        for move in self.moves:
            position = self.robot_position + move

            if self.get(position) != "#" and self.in_bounds(position):
                collisions = [position in box for box in self.boxes]

                if collisions.count(True) > 0:
                    for index, collision in enumerate(collisions):
                        if not collision:
                            continue
                        if len(to_move := self.__check_boxes(index, move)) > 0:
                            for tm in set(to_move):
                                self.boxes[tm] += move
                            self.robot_position = position
                else:
                    self.robot_position = position

    def get_gps_coordinate_sum(self):
        total = 0

        for box in self.boxes:
            total += box.tl.y * 100 + box.tl.x

        return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        layout, moves = file.read().split("\n\n")
        warehouse = Warehouse(layout.splitlines(), moves.replace("\n", ""))
        warehouse.simulate_moves()
        warehouse.print()

        print(
            f"The sum of all boxes' GPS coordinates is {warehouse.get_gps_coordinate_sum()}."
        )

        print()

        warehouse2 = Warehouse(
            layout.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
            .splitlines(),
            moves.replace("\n", ""),
        )
        warehouse2.simulate_moves()
        warehouse2.print()

        print(
            f"The sum of all boxes' GPS coordinates in the second warehouse is {warehouse2.get_gps_coordinate_sum()}."
        )


if __name__ == "__main__":
    main()
