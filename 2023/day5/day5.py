"""
Advent of Code Day 5
"""

import re
import sys


def create_regex(maps: list[str]):
    """
    Creates regex expression to extract maps
    """
    expression = r"seeds: ([\d ]+)"
    for map in maps:
        expression += r"\n\n" + map + r" map:\n([\d\n ]+)"
    return expression


def apply_almanac_map(seed: int, map: list[list[int]]):
    """
    Applies the map to the given seed
    """
    for destination, source, length in map:
        if seed in range(source, source + length):
            return destination + (seed - source)

    return seed


def apply_almanac_map_range(seeds: list[list[int]], map: list[list[int]]):
    """
    Applies the map to a given number of
    """
    new_seeds: list[list[int]] = []

    for seed in seeds:
        has_overlap = False

        for destination, source, length in map:
            map_range = range(source, source + length)
            seed_range = range(seed[0], seed[0] + seed[1])

            overlap = range(
                max(map_range[0], seed_range[0]),
                min(map_range[-1], seed_range[-1]) + 1,
            )

            if len(overlap) > 0:
                offset = destination - source
                overlap_length = len(overlap)
                new_seeds.append([offset + overlap.start, overlap_length])
                has_overlap = True

        if not has_overlap:
            if seed not in new_seeds:
                new_seeds.append(seed)

    return new_seeds


with open(sys.argv[1], encoding="utf-8") as file:
    maps = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    groups = re.search(create_regex(maps), file.read()).groups()

    seeds = [int(seed) for seed in groups[0].split(" ")]
    range_seeds = [
        [seeds[index], seeds[index + 1]] for index in range(0, len(seeds), 2)
    ]

    for group in groups[1:]:
        almanac_map = group.split("\n")

        for index, line in enumerate(almanac_map):
            almanac_map[index] = [int(number) for number in line.split(" ")]

        seeds = list(map(lambda seed: apply_almanac_map(seed, almanac_map), seeds))
        range_seeds = apply_almanac_map_range(range_seeds, almanac_map)

    print("The lowest location number for part 1 is:", min(seeds))
    print(
        "The lowest location number for part 2 is:",
        min([seed[0] for seed in range_seeds]),
    )
