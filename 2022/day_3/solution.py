#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(itertools.islice(it, n)):
        yield batch


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        prios = 0
        for line in data:
            first = set(line[: len(line) // 2])
            second = set(line[len(line) // 2 :])
            item = second & first
            assert len(item) == 1
            item = item.pop()

            if item.lower() == item:
                prio = ord(item) - ord("a") + 1
            else:
                prio = ord(item) - ord("A") + 27
            prios += prio
        return prios

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        prios = 0
        for line1, line2, line3 in batched(data, 3):
            item = set(line1) & set(line2) & set(line3)
            assert len(item) == 1
            item = item.pop()
            if item.lower() == item:
                prio = ord(item) - ord("a") + 1
            else:
                prio = ord(item) - ord("A") + 27
            prios += prio
        return prios

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
