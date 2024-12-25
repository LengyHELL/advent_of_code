"""
Advent of Code Day 23
"""

import sys


def starts_with(char: str, computers: tuple[str, ...]):
    return any([c.startswith(char) for c in computers])


def get_combinations(items: tuple[str, ...], limit=2):
    combinations: list[tuple[str, ...]] = []

    if len(items) <= 1 or limit <= 0:
        return [tuple([items[0]])]

    for index, i in enumerate(items):
        other = items[index + 1 :] + items[: index + 1]
        other = tuple(o for o in other if o != i)
        for c in get_combinations(other, limit - 1):
            combinations.append(tuple(sorted([i, *c])))

    return combinations


def filter_part1(sets: list[tuple[str, ...]]):
    filtered = []

    for s in sets:
        if len(s) == 3:
            filtered.append(s)
        elif len(s) > 3:
            filtered.extend(list(set(get_combinations(s))))

    return [f for f in filtered if starts_with("t", f)]


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        connections: list[tuple[str, ...]] = [
            tuple(line.split("-")) for line in file.read().splitlines()
        ]
        computers: set[str] = set()
        sets: list[set[str]] = []

        for c1, c2 in connections:
            computers.add(c1)
            computers.add(c2)
            sets.append(set([c1, c2]))

        for i, s in enumerate(sets):
            print(f"{i}/{len(sets)}", end="\r")

            for c in computers:
                good = True

                for i in s:
                    if (c, i) not in connections and (i, c) not in connections:
                        good = False
                        break

                if good:
                    s.add(c)

        final: list[tuple[str, ...]] = list(set([tuple(sorted(s)) for s in sets]))
        final = sorted([s for s in final], key="".join)

        part1 = filter_part1(final)

        print(
            f"There are {len(part1)} sets that contain a computer with a name that starts with 't'."
        )

        part2 = sorted(final, key=len, reverse=True)
        password = ",".join(part2[0])

        print(f"The password to get into the LAN party is '{password}'.")

        # TODO: part 1 is not correct after finishing part 2


if __name__ == "__main__":
    main()
