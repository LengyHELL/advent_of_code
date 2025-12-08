"""
Advent of Code 2025 Day 6
"""

import sys


def get_normal_sum(lines: list[str]) -> int:
    lines = [list(filter(len, line.split(" "))) for line in lines]
    operators = [operator for operator in lines[-1]]
    values = [0 if operator == "+" else 1 for operator in operators]

    for l in lines[:-1]:
        for i, _ in enumerate(values):
            if operators[i] == "+":
                values[i] += int(l[i])
            else:
                values[i] *= int(l[i])

    return sum(values)


def get_transposed_sum(lines: list[str]) -> int:
    transposed = [
        "".join([lines[j][i] for j in range(len(lines))]) for i in range(len(lines[0]))
    ]

    operator = ""
    batch = 0
    total = 0

    for i, t in enumerate(transposed):
        try:
            new_operator = t[-1]
            value = int(t[:-1].strip())

            if new_operator != " ":
                total += batch
                operator = new_operator
                batch = value
            else:
                if operator == "+":
                    batch += value
                elif operator == "*":
                    batch *= value

                if i == len(transposed) - 1:
                    total += batch
        except ValueError:
            continue
    return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().splitlines()

        normal_sum = get_normal_sum(lines)

        print(f"The grand total for the worksheet is {normal_sum}.")

        transposed_sum = get_transposed_sum(lines)

        print(f"The grand total for the transposed worksheet is {transposed_sum}.")


if __name__ == "__main__":
    main()
