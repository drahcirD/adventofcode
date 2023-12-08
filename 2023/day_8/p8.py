#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np
import math

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    instr, maps = data
    instr = instr.strip()

    path = collections.defaultdict(dict)
    for d in maps.split("\n"):
        pos, loc = d.split(" = ")
        left, right = loc.split(", ")
        left = left[1:]
        right = right[:-1]
        path[pos]['L'] = left
        path[pos]['R'] = right

    pos = 'AAA'
    while True:
        ins = instr[result % len(instr)]
        if pos == 'ZZZ':
            return result
        pos = path[pos][ins]
        result+=1


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    result = 0
    instr, maps = data
    instr = instr.strip()

    path = collections.defaultdict(dict)
    for d in maps.split("\n"):
        pos, loc = d.split(" = ")
        left, right = loc.split(", ")
        left = left[1:]
        right = right[:-1]
        path[pos]['L'] = left
        path[pos]['R'] = right

    pos = [p for p in path if p[-1] == 'A']
    finishes = {}
    while True:
        ins = instr[result % len(instr)]
        result+=1
        if len(finishes) == len(pos):
           break
        for i, p in enumerate(pos):
            if i in finishes:
                continue
            pos[i] = path[p][ins]
            if pos[i][-1] == 'Z':
                finishes[i] = result
 
    return math.lcm(*finishes.values())


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
