#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    for d in data:
        d = d.split(": ")[1]
        winning, have = d.split(" | ")
        winning = set([int(x.strip()) for x in winning.split(" ") if x.strip()])
        have = set([int(x.strip()) for x in have.split(" ") if x.strip()])
        if have & winning:
            points = 2 ** (len(have & winning) - 1)
            result += points

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    cards = []
    map = {}
    for d in data:
        card, d = d.split(": ")
        card = int(card.split(" ")[-1].strip())

        cards.append(card)
        winning, have = d.split(" | ")
        winning = set([int(x.strip()) for x in winning.split(" ") if x.strip()])
        have = set([int(x.strip()) for x in have.split(" ") if x.strip()])

        map[card] = len(have & winning)

    cards = collections.Counter(cards)
    for c, count in cards.items():
        new = {c + i: count for i in range(1, map[c] + 1) if c + i in map}
        cards.update(new)

    return sum(cards.values())


def main():
    examples = pathlib.Path(__file__).resolve().parent.glob("example*.txt")
    result = collections.defaultdict(dict)
    for example in examples:
        example_data = example.read_text()
        try:
            result["part1"][example.name] = p1(example_data)
        except:
            pass
        try:
            result["part2"][example.name] = p2(example_data)
        except:
            pass

    print()
    print()

    try:
        result["part1"]["input"] = p1(aoc_data)
        result["part2"]["input"] = p2(aoc_data)
    except:
        raise

    pprint(result)

    submit_p1 = input(f'submit p1? {result["part1"]["input"]}')
    if submit_p1.strip().lower() == "y":
        submit(result["part1"]["input"])

    submit_p2 = input(f'submit p2? {result["part2"]["input"]}')
    if submit_p2.strip().lower() == "y":
        submit(result["part2"]["input"])


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path.read_text())


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
