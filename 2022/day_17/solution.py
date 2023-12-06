#! /usr/bin/env python
import operator
import pathlib
from typing import Sequence
import fire
import collections
import itertools
import functools
import dataclasses
import copy


@dataclasses.dataclass
class Rock:
    positions: Sequence[int]

    @property
    def left(self):
        return min(self.positions, key=operator.itemgetter(0))[0]

    @property
    def right(self):
        return max(self.positions, key=operator.itemgetter(0))[0]

    @property
    def top(self):
        return max(self.positions, key=operator.itemgetter(1))[1]

    @property
    def bottom(self):
        return min(self.positions, key=operator.itemgetter(1))[1]

    def shift(self, gust, room):
        adj = 0
        match gust:
            case ">":
                if self.right + 1 == 7:
                    return
                adj = 1
            case "<":
                if self.left - 1 == -1:
                    return
                adj = -1
        new_pos = []
        for pos in self.positions:
            new = (pos[0] + adj, pos[1])
            if new in room:
                return False
            new_pos.append(new)
        self.positions = new_pos
        return True

    def fall(self, room, update=True):
        new_pos = []
        for pos in self.positions:
            new = (pos[0], pos[1] - 1)
            if new in room or new[1] == -1:
                return False
            new_pos.append(new)
        if update:
            self.positions = new_pos
        return True

    def start(self, global_adj):
        self.positions = [
            (x + global_adj[0], y + global_adj[1]) for x, y in self.positions
        ]


def print_room(room, rock=None):

    for y in reversed(range(-1, max(rock.top if rock else 0, max(room, key=operator.itemgetter(1))[1] if room else 0) + 1)):
        for x in range(-1, 8):
            if y == -1:
                print("-", end="")
            elif x == -1 or x == 7:
                print("|", end="")
            elif (x, y) in room:
                print("#", end="")
            elif rock and (x,y) in rock.positions:
                print("@", end='')
            else:
                print(".", end="")
        print()


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        rocks = [
            Rock([(x, 0) for x in range(4)]),
            Rock([(1, 0), (1, 2), *[(x, 1) for x in range(3)]]),
            Rock([*[(x, 0) for x in range(3)], *[(2, y) for y in range(3)]]),
            Rock([(0, x) for x in range(4)]),
            Rock([(x, y) for x in range(2) for y in range(2)]),
        ]
        return path.read_text().strip(), rocks

    def solve(wind, rocks):
        wind = itertools.cycle(wind)
        global_adj = (2, 3)
        room = {}
        for i in range(2022):
            rock = Rock(rocks[i % len(rocks)].positions)
            rock.start(global_adj)
            # print_room(room, rock=rock)
            for gust in wind:
                # print(gust)
                rock.shift(gust, room)
                if not rock.fall(room):
                    for pos in rock.positions:
                        room[(pos[0], pos[1])] = 1
                    break
                # print_room(room, rock=rock)
            global_adj = (2, 3 + max(room, key=operator.itemgetter(1))[1]+1)
            # print(i, global_adj)
            # print_room(room)
            # print()
            # breakpoint()
        return max(room, key=operator.itemgetter(1))+1

    return solve(*parse())

def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        rocks = [
            Rock([(x, 0) for x in range(4)]),
            Rock([(1, 0), (1, 2), *[(x, 1) for x in range(3)]]),
            Rock([*[(x, 0) for x in range(3)], *[(2, y) for y in range(3)]]),
            Rock([(0, x) for x in range(4)]),
            Rock([(x, y) for x in range(2) for y in range(2)]),
        ]
        return path.read_text().strip(), rocks

    def solve(wind, rocks):
        wind = itertools.cycle(wind)
        global_adj = (2, 3)
        room = {}
        prev = 0
        diffs = []
        for i in range(1000000000000):
            if i > 0 and i % len(rocks) == 0:
                height = max(room, key=operator.itemgetter(1))[1]+1
                diffs.append(height-prev)
                prev = height
            
            if i == 50000 :
                print(diffs)
                break
            rock = Rock(rocks[i % len(rocks)].positions)
            rock.start(global_adj)
            for gust in wind:
                rock.shift(gust, room)
                if not rock.fall(room):
                    for pos in rock.positions:
                        room[(pos[0], pos[1])] = 1
                    break
            global_adj = (2, 3 + max(room, key=operator.itemgetter(1))[1]+1)
        
        # manual solve:
        # find repeating section and start section
        # len start = 18
        # len repeat = 344
        # sum(start) + (1000000000000-18*5)//(5*344)*sum(repeat) + sum(repeat[:((1000000000000-18*5)%(5*344))//5])

    return solve(*parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
