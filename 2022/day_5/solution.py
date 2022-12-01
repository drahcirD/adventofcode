#! /usr/bin/env python
import pathlib
from string import whitespace
import fire
import collections
import itertools

def p1(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        stacks, moves = [x for x in path.read_text().split('\n\n')]
        stack_input = list(reversed(stacks.split('\n')))[1:]
        n_stacks = len(stack_input[0].split())
        stack_holder = [list() for _ in range(n_stacks)]
        for line in stack_input:
            i = 0
            whitespace = 0
            print(line.split(' '))
            for c in line.split(' '):
                if not c:
                    whitespace += 1
                    continue
                print(i, c)
                i += whitespace // 3
                stack_holder[i].append(c.replace('[', '').replace(']', ''))
                i += 1
                whitespace = 0
        moves = moves.split('\n')
        return stack_holder, moves
        
    def solve(stacks, moves):
        print(stacks)
        for move in moves:
            print(move)
            move = move.split()
            n, src, dest = (int(move[1]), int(move[3]), int(move[5]))
            print(n, src, dest)
            for i in range(n):
                stacks[dest-1].append(stacks[src-1].pop())
                print(stacks)

        return ''.join([stack.pop() for stack in stacks])
    
    return solve(*parse())

def p2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        stacks, moves = [x for x in path.read_text().split('\n\n')]
        stack_input = list(reversed(stacks.split('\n')))[1:]
        n_stacks = len(stack_input[0].split())
        stack_holder = [list() for _ in range(n_stacks)]
        for line in stack_input:
            i = 0
            whitespace = 0
            print(line.split(' '))
            for c in line.split(' '):
                if not c:
                    whitespace += 1
                    continue
                print(i, c)
                i += whitespace // 3
                stack_holder[i].append(c.replace('[', '').replace(']', ''))
                i += 1
                whitespace = 0
        moves = moves.split('\n')
        return stack_holder, moves
        
    def solve(stacks, moves):
        print(stacks)
        for move in moves:
            print(move)
            move = move.split()
            n, src, dest = (int(move[1]), int(move[3]), int(move[5]))
            print(n, src, dest)
            moved = []
            for i in range(n):
                moved.append(stacks[src-1].pop())
            stacks[dest-1].extend(reversed(moved))

        return ''.join([stack.pop() for stack in stacks])
    
    return solve(*parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    