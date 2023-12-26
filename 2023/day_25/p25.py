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
import networkx as nx
import matplotlib.pyplot as plt

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    connections = collections.defaultdict(set)
    G = nx.Graph()
    for d in data:
        a, b = d.split(": ")
        G.add_node(a)
        for b in b.split(" "):
            G.add_node(b)
            connections[a].add(b)
            G.add_edge(a, b)
        for b in connections[a]:
            connections[b].add(a)
            G.add_edge(b, a)

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=100, node_color='skyblue', font_size=10, font_color='black', edge_color='gray', linewidths=1, alpha=0.7)

    # plt.show()

    if len(connections) > 100:
        cuts = [("pbq", "nzn"), ("xvp", "zpc"), ("dhl", "vfs")]
    else:
        cuts = [("nvd", "jqt"), ("cmg", "bvb"), ("pzl", "hfx")]

    G2 = nx.Graph()

    for cuta, cutb in cuts:
        connections[cuta].remove(cutb)
        connections[cutb].remove(cuta)

    for k, v in connections.items():
        G2.add_node(k)
        for kv in v:
            G2.add_node(kv)
            G2.add_edge(k, kv)
            G2.add_edge(kv, k)

    return reduce(operator.mul, [len(x) for x in nx.connected_components(G2)], 1)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)


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
