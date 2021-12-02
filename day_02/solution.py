#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '02'
DEBUG = False


def parse_input(lines: List[str]) -> List[Tuple[str, int]]:
    def parse(line: str):
        fields = line.strip().split()
        assert fields[0] in {'forward', 'down', 'up'}, \
          "Unrecognized instruction: '{}' in '{}'".format(fields[0], line)
        return (fields[0], int(fields[1]))
    return list(map(parse, lines))


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    x, y = 0, 0
    for cmd, arg in parse_input(lines):
        if cmd == 'forward':
            x += arg
        elif cmd == 'down':
            y += arg
        elif cmd == 'up':
            y -= arg
    return x*y


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    x, y, aim = 0, 0, 0
    for cmd, arg in parse_input(lines):
        if cmd == 'forward':
            x += arg
            y += arg*aim
        elif cmd == 'down':
            aim += arg
        elif cmd == 'up':
            aim -= arg
    return x*y


text_1 = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


tests = [
    (text_1.split('\n'), 15*10, 15*60),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 1762050
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 1855892637
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
