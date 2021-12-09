#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '09'
DEBUG = False


class Board(object):

    AROUND = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @classmethod
    def from_lines(cls, lines: List[str]):
        rows = [list(map(int, line)) for line in lines]
        return cls(rows)

    def __init__(self, rows):
        self.rows = rows

    def dims(self):
        return len(self.rows), len(self.rows[0])

    def __getitem__(self, pos):
        x, y = pos
        if -1 < x < len(self.rows) and -1 < y < len(self.rows[x]):
            return self.rows[x][y]
        return None

    def __iter__(self):
        return self.BoardIterator(self)

    def neighbors_of(self, xy):
        x, y = xy
        for dx, dy in self.AROUND:
            nx, ny = x+dx, y+dy
            val = self[nx, ny]
            if val is not None:
                yield((nx, ny), val)

    class BoardIterator(object):

        def __init__(self, brd):
            self.board = brd
            self.idx = -1
            self.numrows, self.numcols = self.board.dims()

        def __iter__(self):
            return self

        def __next__(self):
            self.idx += 1
            if self.idx < (self.numrows * self.numcols):
                x = int(self.idx / self.numcols)
                y = int(self.idx % self.numcols)
                return (x, y), self.board[x, y]
            raise StopIteration


def find_lowest_points(heightmap):
    higher_points = []
    for pt in heightmap:
        for npt in heightmap.neighbors_of(pt[0]):
            if pt[1] >= npt[1]:
                higher_points.append(pt)
                break

    lowest_points = []
    for pt in heightmap:
        if pt not in higher_points:
            lowest_points.append(pt)

    return lowest_points



def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    heightmap = Board.from_lines(lines)

    lowest_points = find_lowest_points(heightmap)
    risk = sum(pt[1] + 1 for pt in lowest_points)

    return risk


def find_basin(heightmap, lowest):
    basin = {lowest}

    seen_pts = set()
    pts = [lowest]
    while pts:
        for _ in range(len(pts)):
            pt = pts.pop(0)
            for npt in heightmap.neighbors_of(pt[0]):
                if npt in seen_pts:
                    continue
                seen_pts.add(npt)

                if lowest[1] <= npt[1] < 9:
                    pts.append(npt)
                    basin.add(npt)

    return basin


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    heightmap = Board.from_lines(lines)

    sizes = []
    for pt in find_lowest_points(heightmap):
        basin = find_basin(heightmap, pt)
        # print(len(basin), basin)
        sizes.append(len(basin))

    area3 = reduce(lambda a, b: a*b, sorted(sizes)[-3:], 1)

    return area3


text_1 = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""


tests = [
    (text_1.split('\n'), 15, 9 * 14 * 9),
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
    exp1 = 537
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 1142757
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
