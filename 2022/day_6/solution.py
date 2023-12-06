#! /usr/bin/env python
import pathlib
from re import I
import fire
import collections
import itertools


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return path.read_text().strip()

    def solve(data):
        i = 4
        for batch in sliding_window(data, 4):
            if len(set(batch)) == 4:
                return i
            i += 1

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return path.read_text().strip()

    def solve(data):
        i = 14
        for batch in sliding_window(data, 14):
            if len(set(batch)) == 14:
                return i
            i += 1

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
