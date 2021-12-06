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


DAY = '06'
DEBUG = False


def create_fish_school_1(line: str) -> List[list]:
    fishes = map(int, line.split(','))
    return [[f, 1] for f in fishes]


def solve_p1(lines: List[str], days: int = 80) -> int:
    """Solution to the 1st part of the challenge.
    The algorithm mimics the task description.
    """
    fishes = create_fish_school_1(lines[0])
    for d in range(days):
        for i in range(len(fishes)):
            fish = fishes[i]
            if fish[0] == 0:
                fish[0] = 6
                fishes.append([8, 0])  # add a new offspring
            else:
                fish[0] -= 1
        if DEBUG:
            print("After day {}: {}".format(1+d, len(fishes)))
    return len(fishes)


def solve_p2(lines: List[str], days: int = 256) -> int:
    """Solution to the 2nd part of the challenge.

    Uses a different datastructure that is day-based:
    * there are 9 days (0..8)
    * for each day, we keep a count of fish whose timer is at that day
    Thus, for the test case `3,4,3,1,2`, the initial state is:
      [0, 1, 1, 2, 1, 0, 0, 0]
    """

    school = [0] * 9
    for fish in map(int, lines[0].split(',')):
        school[fish] += 1

    if DEBUG:
        print(school)

    for d in range(days):
        # the fish with internal timer 0, as many as <cnt>
        cnt = school.pop(0)
        # they produce <cnt> offsprings
        school.append(cnt)
        # they restart their internal timer
        school[6] += cnt
        if DEBUG:
            print("After day {}, total {}: {}".format(d, sum(school), school))

    return sum(school)


# TODO: solve mathematically? how many fish will a single with with initial counter
# 1 produce in N days?
#solve_p3()


text_1 = "3,4,3,1,2"


tests = [
    (text_1.split('\n'), (18, 26),   (18, 26)),
    (text_1.split('\n'), (80, 5934), (80, 5934)),
    (text_1.split('\n'), None,       (256, 26984457539)),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, exp1[0])
            print(f"T1.{tid}:", res1 == exp1[1], exp1[1], res1)

        if exp2 is not None:
            res2 = solve_p2(inp, exp2[0])
            print(f"T2.{tid}:", res2 == exp2[1], exp2[1], res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 379114
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 1702631502303
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
