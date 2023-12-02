#! /usr/bin/env python
from functools import reduce
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


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    high = {'blue': 14, 'green': 13, 'red': 12}
    for d in data:
        game, d = d.split(':')
        game = int(game.strip().split(' ')[1])
        d = d.split(';')
        possible = True
        for g in d:
            g = g.strip().split(',')
            for item in g:
                n, color = item.strip().split(' ')
                if int(n) > high[color]:
                    possible = False
                    break
        if possible:
            result += game

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    for d in data:
        game, d = d.split(':')
        game = int(game.strip().split(' ')[1])
        d = d.split(';')
        maxes = {'blue': float('-inf'), 'green': float('-inf'), 'red': float('-inf')}
        for g in d:
            g = g.strip().split(',')
            for item in g:
                n, color = item.strip().split(' ')
                maxes[color] = max(maxes[color], int(n))

        result += reduce(operator.mul, maxes.values(), 1)

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
