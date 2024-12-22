"""
Advent of Code Day 21
"""

import sys
from typing import Dict, List, Tuple

from modules.coord import Coord
from modules.grid import Grid


class Node:
    pos: Coord
    prev: "Node"
    direction: Coord

    def __init__(self, pos: Coord, prev: "Node", direction: Coord):
        self.pos = pos
        self.prev = prev
        self.direction = direction

    def get_direction(self):
        if self.direction == Coord(1, 0):
            return ">"
        elif self.direction == Coord(0, 1):
            return "v"
        elif self.direction == Coord(-1, 0):
            return "<"
        elif self.direction == Coord(0, -1):
            return "^"
        else:
            return ""


class NumericKeypad(Grid):
    buttons: Dict[str, Coord]
    current: Coord

    def __init__(self, keypad: List[str]):
        super().__init__(keypad)

        self.buttons = dict()
        self.__init_buttons()
        self.current = self.buttons["A"] if "A" in self.buttons else Coord(0, 0)

    def __init_buttons(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                self.buttons[value] = position

    def get_key_input(self, start: Coord, end: Coord):
        keys = ""
        current = start.copy()
        while current != end:
            diff = end - current

            if diff.x < 0:
                if Coord(end.x, current.y) == self.buttons["#"]:
                    keys += "^" * abs(diff.y)
                    current += Coord(0, diff.y)
                else:
                    keys += "<"
                    current += Coord(-1, 0)
            elif diff.y < 0:
                keys += "^" * abs(diff.y)
                current += Coord(0, diff.y)
            elif diff.y > 0:
                if Coord(current.x, end.y) == self.buttons["#"]:
                    keys += ">" * abs(diff.x)
                    current += Coord(diff.x, 0)
                else:
                    keys += "v"
                    current += Coord(0, 1)
            elif diff.x > 0:
                keys += ">" * abs(diff.x)
                current += Coord(diff.x, 0)
        return keys

    def get_key_presses(self, code: str):
        key_presses: Dict[str, int] = dict()

        for c in code:
            keys = self.get_key_input(self.current, self.buttons[c]) + "A"

            if keys in key_presses:
                key_presses[keys] += 1
            else:
                key_presses[keys] = 1

            self.current = self.buttons[c]

        return key_presses


class DirectionalKeypad(Grid):
    buttons: Dict[str, Coord]
    current: Coord
    moves: Dict[Tuple[str, str], str]

    def __init__(self, keypad: List[str]):
        super().__init__(keypad)

        self.buttons = dict()
        self.__init_buttons()
        self.moves = dict(
            [
                (("A", "^"), "<"),
                (("A", ">"), "v"),
                (("A", "v"), "<v"),
                (("A", "<"), "v<<"),
                (("^", "A"), ">"),
                (("^", ">"), "v>"),
                (("^", "<"), "v<"),
                (("^", "v"), "v"),
                (("v", "A"), "^>"),
                (("v", ">"), ">"),
                (("v", "<"), "<"),
                (("v", "^"), "^"),
                ((">", "A"), "^"),
                ((">", "^"), "<^"),
                ((">", "v"), "<"),
                ((">", "<"), "<<"),
                (("<", "A"), ">>^"),
                (("<", "^"), ">^"),
                (("<", "v"), ">"),
                (("<", ">"), ">>"),
            ]
        )

    def __init_buttons(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                self.buttons[value] = position

    def get_key_input_old(self, start: Coord, end: Coord):
        keys = ""
        diff = end - start

        if diff.y > 0:
            keys += "v" * diff.y
        if diff.x > 0:
            keys += ">" * diff.x
        if diff.y < 0:
            keys += "^" * -diff.y
        if diff.x < 0:
            keys += "<" * -diff.x

        return keys

    def get_key_input(self, start: Coord, end: Coord):
        if start == end:
            return ""
        else:
            return self.moves[self.get(start), self.get(end)]

    def get_key_presses(self, other_presses: Dict[str, int]):
        key_presses: Dict[str, int] = dict()

        for code, count in other_presses.items():
            self.current = self.buttons["A"]
            for c in code:
                keys = self.get_key_input(self.current, self.buttons[c]) + "A"

                if keys in key_presses:
                    key_presses[keys] += count
                else:
                    key_presses[keys] = count

                self.current = self.buttons[c]

        return key_presses


def get_complexity(codes: List[str], directional_keypads: int):
    numeric_keypad = NumericKeypad(["789", "456", "123", "#0A"])
    directional_keypad = DirectionalKeypad(["#^A", "<v>"])

    sum_of_complexities = 0

    for code in codes:
        key_presses = numeric_keypad.get_key_presses(code)

        for _ in range(directional_keypads):
            key_presses = directional_keypad.get_key_presses(key_presses)

        complexity = 0
        for key, count in key_presses.items():
            complexity += count * len(key)

        sum_of_complexities += complexity * int(code[:-1])
    return sum_of_complexities


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        codes = file.read().splitlines()

        calculations = [2, 25]

        for c in calculations:
            d = get_complexity(codes, c)
            print(
                f"The sum of complexities of the five codes with {c} directional keypads is {d}."
            )


if __name__ == "__main__":
    main()
