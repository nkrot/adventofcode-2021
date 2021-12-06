#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '05'
DEBUG = False


def parse_input(lines: List[str]) -> List[tuple]:
    segments = []
    for line in lines:
        if line:
            fields = list(map(int, re.sub(r'[^\d]+', ' ', line).split()))
            pt1 = (fields[0], fields[1])
            pt2 = (fields[2], fields[3])
            segments.append((pt1, pt2))
    if DEBUG:
        print("--- Line segments ---")
        print(segments)
    return segments


def points_between(startp, endp):
    """Generate all points between given two points <startp> and <endp>."""

    def _step(s, e):
        return 1 if s <= e else -1

    x1, y1 = startp
    x2, y2 = endp

    xstep = _step(x1, x2)
    xrange = range(x1, x2 + xstep, xstep)

    ystep = _step(y1, y2)
    yrange = range(y1, y2 + ystep, ystep)

    if x1 == x2:
        xrange = [x1] * len(yrange)
    if y1 == y2:
        yrange = [y1] * len(xrange)

    for x, y in zip(xrange, yrange):
        yield((x, y))


def solve_p1(lines: List[str], part=1) -> int:
    """Solution to the 1st part of the challenge"""
    segments = parse_input(lines)

    points = defaultdict(int)
    for pt1, pt2 in segments:
        if part == 1 and pt1[0] != pt2[0] and pt1[1] != pt2[1]:
            # skip cases that are neither vertical nor horizontal
            continue

        for pt in points_between(pt1, pt2):
            points[pt] += 1

    res = len([1 for pt, cnt in points.items() if cnt > 1])

    return res


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 2)


text_1 = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


tests = [
    (text_1.split('\n'), 5, 12),
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
    exp1 = 7380
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 21373
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
