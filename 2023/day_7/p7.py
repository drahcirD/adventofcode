#! /usr/bin/env python
import functools
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


ORDER = list((["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
ORDER2 = list((["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]))


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    five = []
    four = []
    full = []
    three = []
    two = []
    one = []
    high = []
    bids = {}

    for d in data:
        hand, bid = d.split()
        count = collections.Counter(hand)
        bids[hand] = int(bid)

        if max(count.values()) == 5:
            five.append(hand)
        elif max(count.values()) == 4:
            four.append(hand)
        elif max(count.values()) == 3 and len(count) == 2:
            full.append(hand)
        elif max(count.values()) == 3:
            three.append(hand)
        elif len([k for k, v in count.items() if v == 2]) == 2:
            two.append(hand)
        elif len([k for k, v in count.items() if v == 2]) == 1:
            one.append(hand)
        elif len(set(str(hand))) == len(str(hand)):
            high.append(hand)
        else:
            breakpoint()
    rank = 1

    def cmp(a, b):
        for x, y in zip(a, b):
            if x == y:
                continue
            if ORDER.index(x) < ORDER.index(y):
                return -1
            else:
                return 1

    key = functools.cmp_to_key(cmp)
    for h in reversed(sorted(high, key=key)):
        result += rank * bids[h]
        print(h, rank)
        rank += 1
    for h in reversed(sorted(one, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(two, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(three, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(full, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(four, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(five, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    five = []
    four = []
    full = []
    three = []
    two = []
    one = []
    high = []
    bids = {}

    for d in data:
        hand, bid = d.split()
        count = collections.Counter(hand)
        bids[hand] = int(bid)
        n_J = len([c for c in hand if c == "J"])
        if (
            max(count.values()) == 5
            or max([v for k, v in count.items() if k != "J"]) + count["J"] == 5
        ):
            five.append(hand)
        elif (
            max(count.values()) == 4
            or max([v for k, v in count.items() if k != "J"]) + count["J"] == 4
        ):
            four.append(hand)
        elif (
            max(count.values()) == 3
            and len(count) == 2
            or (
                len([k for k, v in count.items() if v == 2 and k != "J"]) == 2
                and n_J == 1
            )
        ):
            full.append(hand)
        elif (
            max(count.values()) == 3
            or max([v for k, v in count.items() if k != "J"]) + count["J"] == 3
        ):
            three.append(hand)
        elif len([k for k, v in count.items() if v == 2]) == 2 or n_J == 2:
            two.append(hand)
        elif len([k for k, v in count.items() if v == 2]) == 1 or "J" in hand:
            one.append(hand)
        elif len(set(str(hand))) == len(str(hand)):
            high.append(hand)
        else:
            breakpoint()
    rank = 1

    def cmp(a, b):
        for x, y in zip(a, b):
            if x == y:
                continue
            if ORDER2.index(x) < ORDER2.index(y):
                return -1
            else:
                return 1

    key = functools.cmp_to_key(cmp)
    for h in reversed(sorted(high, key=key)):
        result += rank * bids[h]
        print(h, rank)
        rank += 1
    for h in reversed(sorted(one, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(two, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(three, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(full, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(four, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1
    for h in reversed(sorted(five, key=key)):
        result += rank * bids[h]
        print(h, rank)

        rank += 1

    return result


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
