#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '07'
DEBUG = False


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    positions = sorted(list(map(int, line.split(','))))
    total_fuels = []
    for alpos in set(positions):
        total_fuels.append(sum(abs(alpos-pos) for pos in positions))
    return min(total_fuels)


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""

    #   | time -p |
    # 1 | 17,01   |
    # 2 |  0,50   | with memoization
    # 3 |  0,48   | with more complex memoization

    def compute_fuel_1(sp, ep):
        d = abs(sp - ep)
        return sum(range(1, 1+d))

    def compute_fuel_2(sp, ep, memo={}):
        d = abs(sp - ep)
        if d not in memo:
            memo[d] = sum(range(1, 1+d))
        return memo[d]

    def compute_fuel_3(sp, ep, memo={}):
        d = abs(sp - ep)
        if d not in memo:
            _d = d - 1
            if _d in memo:  # 638 times
                memo[d] = memo[_d] + d
            else:           # 1353 times
                memo[d] = sum(range(1, 1+d))
        return memo[d]

    positions = sorted(list(map(int, line.split(','))))
    mn, mx = utils.minmax(positions)
    total_fuels = []
    for alpos in range(mn, 1+mx):
        total_fuels.append(sum(compute_fuel_3(alpos, pos) for pos in positions))

    return min(total_fuels)


text_1 = "16,1,2,0,4,2,7,1,2,14"

tests = [
    (text_1, 37, 168),
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
    lines = utils.load_input()[0]

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 337833
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 96678050
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
