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
from tqdm import tqdm


def parse(data):
    lines = [x for x in data.split("\n\n")]
    return lines[0].split(", "), lines[1].split("\n")


@functools.lru_cache()
def dfs(design, towels):
    if not design:
        return True

    for t in towels:
        if design[: len(t)] == t:
            if dfs(design[len(t) :], towels):
                return True
    return False


def p1(data=aoc_data):
    towels, designs = parse(data)

    result = 0

    for design in tqdm(designs):
        result += dfs(design, tuple(towels))

    return result


def parse2(data):
    return parse(data)


@functools.lru_cache()
def dfs2(design, towels):
    if not design:
        return 1

    ret = 0
    for t in towels:
        if design[: len(t)] == t:
            ret += dfs2(design[len(t) :], towels)

    return ret


def p2(data=aoc_data):
    towels, designs = parse2(data)

    result = 0

    for design in designs:
        result += dfs2(design, tuple(towels))

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
