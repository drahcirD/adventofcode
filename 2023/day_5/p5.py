#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools


from aocd import data as aoc_data
from aocd import submit
from ranges import Range, RangeSet


def parse(data):
    lines = [x for x in data.split("\n\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = float("inf")

    seeds = data[0].split(":")[1].strip().split()

    maps = collections.defaultdict(lambda: collections.defaultdict(list))
    for entry in data[1:]:
        entry = entry.split("\n")
        src, dst = entry[0].split()[0].split("-to-")
        for range_entry in entry[1:]:
            dst_range, src_range, length = [int(n) for n in range_entry.split()]

            maps[src][dst].append(
                lambda n, dst_range=dst_range, src_range=src_range, length=length: dst_range
                + (n - src_range)
                if src_range <= n < src_range + length
                else n
            )

    for d in seeds:
        src = "seed"
        dst = "soil"
        cur_n = int(d)
        while dst != "location":
            for f in maps[src][dst]:
                new_n = f(cur_n)
                print(f"{new_n}")
                if new_n != cur_n:
                    cur_n = new_n
                    break
            src = dst
            dst = list(maps[dst].keys())[0]

        for f in maps[src][dst]:
            new_n = f(cur_n)
            if new_n != cur_n:
                cur_n = new_n
                break

        result = min(result, cur_n)
    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = float("inf")

    seeds = data[0].split(":")[1].strip().split()
    seed_range = RangeSet()
    for i in range(0, len(seeds), 2):
        seed_range.add(Range(int(seeds[i]), int(seeds[i]) + int(seeds[i + 1])))

    maps = []
    for entry in data[1:]:
        entry = entry.split("\n")
        maps.append([])
        for range_entry in entry[1:]:
            dst_range, src_range, length = [int(n) for n in range_entry.split()]

            maps[-1].append((dst_range, src_range, length))

    result = 0

    while True:
        cur_n = result
        for translation in reversed(maps):
            for dst_range, src_range, length in translation:
                if dst_range <= cur_n < dst_range + length:
                    cur_n = src_range + (cur_n - dst_range)
                    break

        if cur_n in seed_range:
            return result
        result += 1


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
