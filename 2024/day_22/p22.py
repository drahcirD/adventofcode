#! /usr/bin/env python
import functools
import operator
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit
import sympy


def parse(data):
    lines = [int(x) for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    for secret in data:
        d = secret
        for i in range(2000):
            d = (d * 64) ^ d
            d &= 16777216 - 1
            d = (d // 32) ^ d
            d &= 16777216 - 1
            d = (d * 2048) ^ d
            d &= 16777216 - 1
        result += d

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    values = []
    for secret in data:
        d = secret
        prices = [d % 10]
        cur_values = {}
        values.append(cur_values)
        for i in range(2000):
            d = (d * 64) ^ d
            d &= 16777216 - 1
            d = (d // 32) ^ d
            d &= 16777216 - 1
            d = (d * 2048) ^ d
            d &= 16777216 - 1
            prices.append(d % 10)

        for i in range(4, len(prices)):
            seq = (
                prices[i - 3] - prices[i - 4],
                prices[i - 2] - prices[i - 3],
                prices[i - 1] - prices[i - 2],
                prices[i] - prices[i - 1],
            )

            if seq not in cur_values:
                cur_values[seq] = prices[i]

    best = 0
    all_seqs = set(values[0])

    for seqs in values:
        all_seqs |= set(seqs)

    for seq in all_seqs:
        cur = 0
        for vals in values:
            cur += vals.get(seq, 0)

        best = max(best, cur)

    return best


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
