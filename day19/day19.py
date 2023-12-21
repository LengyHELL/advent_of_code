"""
Advent of Code Day 19
"""

import sys
import re
from typing import Callable


class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, data: str):
        variables = data.strip("{}").split(",")
        for variable in variables:
            label, value = variable.split("=")
            setattr(self, label, int(value))

    def __str__(self):
        return f"(x={self.x}, m={self.m}, a={self.a}, s={self.s})"

    def __repr__(self):
        return self.__str__()

    def get_rating(self):
        return self.x + self.m + self.a + self.s

    def copy(self):
        return Part(f"{{x={self.x},m={self.m},a={self.a},s={self.s}}}")


class Rule:
    variable: str = None
    operation: str = None
    compare: int = None
    result: str = None
    __operations: dict[str, Callable[[int, int], bool]] = {
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
    }
    __off_range: dict[str, int] = {}

    def __init__(self, data: str):
        try:
            expression, self.result = data.split(":")
            self.variable, self.operation, compare_string = re.search(
                r"([xmas])(.)(\d+)", expression
            ).groups()

            self.compare = int(compare_string)
            self.__off_range = {
                "<": self.compare - 1 if self.compare else 0,
                ">": self.compare + 1 if self.compare else 0,
            }
        except ValueError:
            self.result = data

    def __str__(self):
        if self.variable is not None:
            return f"({self.variable} {self.operation} {self.compare} -> {self.result})"
        else:
            return f"(--> {self.result})"

    def __repr__(self):
        return self.__str__()

    def calculate(self, part: Part):
        if self.variable is None:
            return self.result

        if self.__operations[self.operation](
            getattr(part, self.variable), self.compare
        ):
            return self.result

        return None

    def calculate_range(self, min_part: Part, max_part: Part):
        if self.variable is None:
            return {self.result: (min_part, max_part)}

        if self.calculate(min_part) is None:
            accepted = min_part.copy()
            rejected = max_part.copy()
            setattr(accepted, self.variable, self.__off_range[self.operation])
            setattr(rejected, self.variable, self.compare)
            return {self.result: (accepted, max_part), None: (min_part, rejected)}
        else:
            accepted = max_part.copy()
            rejected = min_part.copy()
            setattr(accepted, self.variable, self.__off_range[self.operation])
            setattr(rejected, self.variable, self.compare)
            return {self.result: (min_part, accepted), None: (rejected, max_part)}


class Workflow:
    rules: list[Rule]

    def __init__(self, data: str):
        self.rules = [Rule(rule_string) for rule_string in data.strip("{}").split(",")]

    def __str__(self):
        print_string = "Workflow:"
        for rule in self.rules:
            print_string += f"\n\t{rule}"

        return print_string

    def __repr__(self):
        return f"<workflow [{len(self.rules)} rules]>"

    def run(self, part: Part):
        for rule in self.rules:
            if result := rule.calculate(part):
                return result
        return None

    def run_range(self, min_part: Part, max_part: Part):
        current_min = min_part.copy()
        current_max = max_part.copy()
        total_results: dict[str | None, list[tuple[Part, Part]]] = {}
        none_result = None

        for rule in self.rules:
            results = rule.calculate_range(current_min, current_max)

            none_result = None
            try:
                none_result = results.pop(None)
            except KeyError:
                pass

            for key, result in results.items():
                if key in total_results:
                    total_results[key].append(result)
                else:
                    total_results[key] = [result]

            if none_result is not None:
                current_min, current_max = none_result
            else:
                break

        if none_result is not None:
            total_results[None] = [none_result]

        return total_results


def get_range_size(min_part: Part, max_part: Part):
    attributes = "xmas"
    total = 1
    for attribute in attributes:
        size = getattr(max_part, attribute) - getattr(min_part, attribute) + 1
        if size < 0:
            size = 0
        total *= size
    return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        workflow_string, part_string = file.read().split("\n\n")

        workflows = dict[str, Workflow]()
        for name, data in re.findall(r"([a-z]+)\{(\S+)\}", workflow_string):
            workflows[name] = Workflow(data)

        parts = [Part(data) for data in part_string.split("\n")]
        total_ratings = 0

        for part in parts:
            try:
                workflow = workflows["in"]
                result: str = None

                while True:
                    result = workflow.run(part)
                    if result in "AR":
                        break
                    elif result is not None:
                        workflow = workflows[result]
                    else:
                        break

                if result == "A":
                    total_ratings += part.get_rating()
            except KeyError as error:
                print(f"No workflow named {error}!")

        print(f"The sum of ratings is {total_ratings}")

        queue: list[tuple(str, tuple[Part, Part])] = [
            ("in", (Part("{x=1,m=1,a=1,s=1}"), Part("{x=4000,m=4000,a=4000,s=4000}")))
        ]
        accepted: list[tuple[Part, Part]] = []
        try:
            while len(queue) > 0:
                label, (min_part, max_part) = queue.pop(0)
                results = workflows[label].run_range(min_part, max_part)

                if len(results) <= 0:
                    break

                if "A" in results:
                    accepted.extend(results["A"])

                for key, result in results.items():
                    if key in "AR":
                        continue
                    for ranges in result:
                        queue.append((key, ranges))

        except KeyError as error:
            print(f"No workflow named {error}!")

        accepted_parts = 0
        for min_part, max_part in accepted:
            accepted_parts += get_range_size(min_part, max_part)

        print("The number of accepted ratings")
        print(f"\tfrom {Part('{x=1,m=1,a=1,s=1}')}")
        print(f"\tto {Part('{x=4000,m=4000,a=4000,s=4000}')}")
        print(f"is {accepted_parts}")


if __name__ == "__main__":
    main()
