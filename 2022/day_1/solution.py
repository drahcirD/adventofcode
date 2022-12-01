#! /usr/bin/env python
import pathlib
import fire

def p1(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        nbrs =  [[int(x) for x in y.split('\n')] for y in path.read_text().split('\n\n')]
        return nbrs
        
    def solve(data):
        return max([sum(x) for x in data])
    
    return solve(parse())

def p2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        nbrs =  [[int(x) for x in y.split('\n')] for y in path.read_text().split('\n\n')]
        return nbrs
        
    def solve(data):
        return sum(sorted([sum(x) for x in data])[-3:])
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    