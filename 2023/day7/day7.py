"""
Advent of Code Day 7
"""

import re
import sys
from functools import cmp_to_key


def get_values(cards: str):
    values = {}

    for card in cards:
        if card in values:
            values[card] += 1
        else:
            values[card] = 1

    return values


def comparator(hand_a: tuple[str, int], hand_b: tuple[str, int], use_joker=False):
    values_a = get_values(hand_a[0])
    values_b = get_values(hand_b[0])

    deck = "23456789TJQKA"  # card values in ascending order

    if use_joker:
        deck = "J23456789TQKA"

        if len(values_a) > 1:
            joker = values_a.pop("J", 0)
            values_a[max(values_a, key=lambda x: values_a[x])] += joker

        if len(values_b) > 1:
            joker = values_b.pop("J", 0)
            values_b[max(values_b, key=lambda x: values_b[x])] += joker

    scores_a = sorted(list(values_a.values()), reverse=True)
    scores_b = sorted(list(values_b.values()), reverse=True)

    score_a = scores_a[0]
    score_b = scores_b[0]

    if score_a == score_b:
        if len(scores_a) > 1:
            score_a += scores_a[1]

        if len(scores_b) > 1:
            score_b += scores_b[1]

    index = 0
    while score_a == score_b and index < 5:
        score_a += deck.find(hand_a[0][index])
        score_b += deck.find(hand_b[0][index])
        index += 1

    if score_a < score_b:
        return -1
    if score_b < score_a:
        return 1
    else:
        return 0


with open(sys.argv[1], encoding="utf-8") as file:
    lines = file.read().split("\n")
    hands: list[tuple[str, int]] = []

    for line in lines:
        cards, bid_string = re.search(r"([AKQJT98765432]{5}) (\d+)", line).groups()
        bid = int(bid_string)
        hands.append((cards, bid))

    normal = sorted(hands, key=cmp_to_key(comparator))
    joker = sorted(hands, key=cmp_to_key(lambda a, b: comparator(a, b, True)))

    normal_winnings = 0
    joker_winnings = 0
    for index in range(len(hands)):
        normal_winnings += (index + 1) * normal[index][1]
        joker_winnings += (index + 1) * joker[index][1]

    print("The total winnings are:", normal_winnings)
    print("The total winnings with jokers are:", joker_winnings)
