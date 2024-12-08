"""
Advent of Code Day 8
"""

import sys
from typing import List, Dict

from termcolor import colored

from modules.coord import Coord
from modules.grid import Grid


class AntennaMap(Grid):
    antennas: Dict[str, List[Coord]] = dict()
    antinodes: List[Coord]

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)

        self.antinodes = []
        self.find_antennas()

    def draw_cell(self, position):
        value = self.get(position)

        if position in self.antinodes:
            return colored(value, "white", "on_blue")
        else:
            return value

    def find_antennas(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if value != ".":
                    if value in self.antennas:
                        self.antennas[value].append(position)
                    else:
                        self.antennas[value] = [position]

    def find_antinodes(self):
        self.antinodes = []
        for positions in self.antennas.values():
            for index, position in enumerate(positions):
                for other in positions[index + 1 :]:
                    diff = other - position

                    if (
                        self.constrain(temp := other + diff) == temp
                        and temp not in self.antinodes
                    ):
                        self.antinodes.append(temp)
                    if (
                        self.constrain(temp := position - diff) == temp
                        and temp not in self.antinodes
                    ):
                        self.antinodes.append(temp)

    def find_antinodes_with_resonance(self):
        self.antinodes = []
        for positions in self.antennas.values():
            for index, position in enumerate(positions):
                for other in positions[index + 1 :]:
                    diff = other - position

                    i = 0
                    while self.constrain(temp := other + diff * i) == temp:
                        if temp not in self.antinodes:
                            self.antinodes.append(temp)
                        i += 1

                    i = 0
                    while self.constrain(temp := position - diff * i) == temp:
                        if temp not in self.antinodes:
                            self.antinodes.append(temp)
                        i += 1


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        antenna_map = AntennaMap(file.read().splitlines())
        antenna_map.find_antinodes()
        antenna_map.print()

        print(
            f"There are {len(antenna_map.antinodes)} unique locations with antinodes."
        )

        antenna_map.find_antinodes_with_resonance()
        antenna_map.print()

        print(
            f"There are {len(antenna_map.antinodes)} unique locations with antinodes, including resonant harmonics."
        )


if __name__ == "__main__":
    main()
