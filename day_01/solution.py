#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '01'
DEBUG = False


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    nums = utils.to_numbers(lines)
    res = list(filter(lambda x: x[0] < x[1], zip(nums, nums[1:])))
    return len(res)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    nums = utils.to_numbers(lines)
    triples = list(map(sum, zip(nums, nums[1:], nums[2:])))
    return solve_p1(triples)


text_1 = """199
200
208
210
200
207
240
269
260
263"""


tests = [
    (text_1.split('\n'), 7, 5),
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
    exp1 = 1154
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 1127
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
