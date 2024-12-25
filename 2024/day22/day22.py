"""
Advent of Code Day 22
"""

import sys


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        secret_numbers = list(map(int, file.read().splitlines()))
        sum_of_secret_numbers = 0
        all_sequences: dict[tuple[int, ...], int] = dict()

        for sn in secret_numbers:
            sequences: dict[tuple[int, ...], int] = dict()
            numbers: list[int] = []
            previous = None

            for _ in range(2000):
                sn = ((sn * 64) ^ sn) % 16777216
                sn = (int(sn / 32) ^ sn) % 16777216
                sn = ((sn * 2048) ^ sn) % 16777216

                current = int(str(sn)[-1])
                if previous is not None:
                    numbers.append(current - previous)
                previous = current

                if len(numbers) >= 4:
                    sequence = tuple(numbers)

                    if sequence not in sequences:
                        sequences[sequence] = current

                    numbers.pop(0)

            sum_of_secret_numbers += sn
            for s, i in sequences.items():
                if s in all_sequences:
                    all_sequences[s] += i
                else:
                    all_sequences[s] = i

        most_bananas = sorted(all_sequences.values(), reverse=True)[0]

        print(
            f"The sum of the 2000th secret number generated by each buyer is {sum_of_secret_numbers}."
        )

        print(f"The most bananas we can get is {most_bananas}.")


if __name__ == "__main__":
    main()