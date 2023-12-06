#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools

def e1(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)

def e2(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)

def p1(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [int(x) for x in path.read_text().split('\n')]
        return lines
        
    def solve(data):
        pass
    
    return solve(parse())

def p2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        return []
        
    def solve(data):
        pass
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    