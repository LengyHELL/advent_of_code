"""
Advent of Code Day 19
"""

import sys
import re
from functools import cache


class Design:
    value: str
    options: dict[int, list[str]]

    def __init__(self, value: str, towels: list[str]):
        self.value = value
        self.options = dict()

        self.__init_options(towels)

    def __init_options(self, towels: list[str]):
        for towel in towels:
            result = findall(self.value, towel)

            for item in result:
                if item in self.options:
                    self.options[item].append(towel)
                else:
                    self.options[item] = [towel]

    @cache
    def possible_options(self, index=0):
        possible = 0

        if index >= len(self.value):
            possible += 1

        if index in self.options:
            for option in self.options[index]:
                if self.value[index:].startswith(option):
                    possible += self.possible_options(index + len(option))

        return possible


def findall(string: str, sub: str):
    regex = f"(?={sub})"
    return [i.start() for i in re.finditer(regex, string)]


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        towel_data, design_data = file.read().split("\n\n")
        towels = sorted(towel_data.split(", "), key=len, reverse=True)
        designs = design_data.splitlines()

        possible = 0
        all_possible = 0

        for design in designs:
            current = Design(design, towels)

            found = current.possible_options()

            all_possible += found

            if found > 0:
                possible += 1

        print(f"There are {possible} possible designs.")
        print(f"The sum of all the different combinations is {all_possible}.")


if __name__ == "__main__":
    main()
