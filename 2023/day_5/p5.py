#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools



from aocd import data as aoc_data
from aocd import submit
import tqdm

# seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4


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
    new_seeds = []
    
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

    for i in tqdm.tqdm(range(0, len(seeds), 2), desc=" outer", position=0):
        for d in tqdm.tqdm(range(int(seeds[i]), int(seeds[i])+int(seeds[i + 1])), desc=" inner loop", position=1, leave=False):
            src = "seed"
            dst = "soil"
            cur_n = int(d)
            while dst != "location":
                for f in maps[src][dst]:
                    new_n = f(cur_n)
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
        print("cur result = ", result)
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
