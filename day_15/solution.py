#!/usr/bin/env python

# # #
#
# TODO
# 1. try using heapq instead of PriorityQueue. what is faster?
#

import re
import os
import sys
from typing import List
from queue import PriorityQueue
from copy import deepcopy

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils
from day_09.solution import Board


DAY = '15'
DEBUG = False


def compute_risks(board, startp, endp):
    # came_from = {startp: None}
    risk_so_far = {startp: 0}

    frontier = PriorityQueue()  # lowest first
    frontier.put((0, startp))

    while frontier.qsize():
        _, pt = frontier.get()

        # print("Current", pt, risk_so_far[pt])
        if pt == endp:
            # print("Reached", pt, risk_so_far[pt])
            break

        for neigh in board.neighbors_of(pt):
            coord, risk = neigh
            # if coord in came_from:
            #     continue
            # print("..", neigh)
            new_risk = risk_so_far[pt] + risk
            if coord not in risk_so_far or new_risk < risk_so_far[coord]:
                # came_from[coord] = pt
                risk_so_far[coord] = new_risk
                frontier.put((new_risk, coord))

    return risk_so_far[endp]


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    cavern = Board.from_lines(lines)
    h, v = cavern.dims()
    return compute_risks(cavern, (0, 0), (h-1, v-1))


def expand_cavern(base: Board):
    """Expand the cavern to be 5x5 by repeating the base cavern to the right
    and downwards.
    """
    # What can be changed:
    # TODO: this all can be done easier with numpy (hstack, vstack)
    # TODO: create an empty megacavern of final size and populate it
    rows = [[], [], [], [], []]
    for ri in range(5):
        for ci in range(5):
            tile = deepcopy(base)
            for coord, value in tile:
                value += (ri+ci)
                tile[coord] = value - 9 if value > 9 else value
            rows[ri].append(tile)

    if DEBUG:
        text = ""
        pos = (0, 0)
        for ri in range(len(rows)):
            for ci in range(len(rows[ri])):
                tile = rows[ri][ci]
                text += " {}".format(tile[pos])
            text += "\n"
        print(text)

    for ri in range(len(rows)):
        megatile = rows[ri].pop(0)
        while rows[ri]:
            # merge tile into another tile
            other = rows[ri].pop(0)
            for i, r in enumerate(other.rows):
                megatile.rows[i].extend(r)
        # print(megatile)
        # print("---")
        rows[ri] = megatile

    megatile = rows.pop(0)
    while rows:
        other = rows.pop(0)
        megatile.rows.extend(other.rows)
    
    #print(megatile.dims())
    return megatile


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    cavern = Board.from_lines(lines)
    megacavern = expand_cavern(cavern)
    h, v = megacavern.dims()
    return compute_risks(megacavern, (0, 0), (h-1, v-1))


tests = [
    (utils.load_input("test.1.txt"), 40, 315),
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
    exp1 = 602
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 2935
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
