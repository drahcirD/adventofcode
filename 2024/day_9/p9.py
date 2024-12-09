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
    lines = [int(x) for x in data]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0
    blocks = [(i // 2, x) for i, x in enumerate(data) if i % 2 == 0]
    free = list(reversed([x for i, x in enumerate(data) if i % 2 == 1]))

    index = 0
    i = 0
    id, block = blocks.pop()
    while blocks and free:
        if i < len(blocks):
            b_id, b = blocks[i]
            result += (index * b_id + (index + b - 1) * b_id) * b / 2
            index += b
            i += 1

        if free:
            cur_free = free.pop()
            while cur_free > 0:
                if i > id:
                    break
                if cur_free >= block:
                    cur_free -= block
                    result += (index * id + (index + block - 1) * id) * block / 2
                    index += block
                    id, block = blocks.pop()
                else:
                    result += (index * id + (index + cur_free - 1) * id) * cur_free / 2
                    index += cur_free
                    block -= cur_free
                    cur_free = 0

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    blocks = [(i // 2, x) for i, x in enumerate(data) if i % 2 == 0]
    free = [(i // 2, x) for i, x in enumerate(data) if i % 2 == 1]

    index = 0
    start_blocks = {}
    start_free = {}
    bid_to_b = {}
    for block, f in itertools.zip_longest(blocks, free):
        if block:
            (bid, block) = block
            start_blocks[bid] = index
            bid_to_b[bid] = block
            index += block
        if f:
            (fid, f) = f
            start_free[fid] = index
            index += f

    inserted = collections.defaultdict(list)
    inserts = {}
    for bid, block in reversed(blocks):
        for fid, f in free:
            if f >= block and start_blocks[bid] > start_free[fid]:
                inserted[fid].append(bid)

                free[fid] = (fid, f - block)
                inserts[bid] = fid
                break

    for bid, block in blocks:
        if bid not in inserts:
            index = start_blocks[bid]
        else:
            index = start_free[inserts[bid]]
            insert_index = inserted[inserts[bid]].index(bid)
            for otherblockid in inserted[inserts[bid]][:insert_index]:
                index += bid_to_b[otherblockid]

        result += (index * bid + (index + block - 1) * bid) * block / 2

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
