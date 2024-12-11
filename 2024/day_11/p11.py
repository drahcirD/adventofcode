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
from tqdm import tqdm


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    cur = data[0].split(" ")
    for i in range(1, 26):
        new = []
        for d in cur:
            if d == "0":
                new.append("1")
            elif len(d) % 2 == 0:
                new.append(d[: len(d) // 2])
                b = d[len(d) // 2 :].lstrip("0")
                new.append(b if b else "0")
            else:
                new.append(str(int(d) * 2024))
        cur = new

    return len(cur)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    cur = collections.Counter(data[0].split(" "))
    for i in range(1, 76):
        new = collections.Counter()
        for d in cur:
            if d == "0":
                new["1"] += cur[d]
            elif len(d) % 2 == 0:
                new[d[: len(d) // 2]] += cur[d]
                b = d[len(d) // 2 :].lstrip("0")
                new[b if b else "0"] += cur[d]
            else:
                new[str(int(d) * 2024)] += cur[d]
        cur = new
    return sum(cur.values())


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
