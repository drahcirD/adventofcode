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
        cur = [int(x) for x in d.split()]
        inc = set()
        for a,b in itertools.pairwise(cur):
            if a == b:
                break
            if 3 < abs(a-b):
                break

            if a-b > 0:
                inc.add(1)
            elif a-b < 0:
                inc.add(0)
            
            if len(inc) > 1:
                break
        else:
            print(cur)
            result += 1

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    result = 0

    for d in data:
        cur = [int(x) for x in d.split()]
        safe = False
        for i in range(len(cur)):
            inc = set()
            cur2 = cur[:i] + cur[i+1:]
            for a,b in itertools.pairwise(cur2):
                if a == b:
                    break
                if 3 < abs(a-b):
                    break

                if a-b > 0:
                    inc.add(1)
                elif a-b < 0:
                    inc.add(0)
                
                if len(inc) > 1:
                    break
            else:
                safe = True
            if safe:
                result +=1
                break
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
