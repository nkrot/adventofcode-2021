#!/usr/bin/env python

# # #
#
# #

import os
import sys
from typing import List
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '14'
DEBUG = False


def parse_input(lines:  List[str]):
    rules = {}
    polymer = defaultdict(int)
    charcounts = defaultdict(int)
    for line in lines:
        if not line:
            continue
        if line and '->' in line:
            pair, _, ins = line.split()
            if pair in rules:
                raise ValueError(f"Key already exists in: {pair}")
            rules[pair] = ins
        else:
            for i in range(len(line)-1):
                pair = line[i:2+i]
                polymer[pair] += 1
                charcounts[line[i:1+i]] += 1
            charcounts[line[-1]] += 1
    return polymer, rules, charcounts


def solve_p1(lines: List[str], steps: int = 10) -> int:
    """Solution to the 1st part of the challenge"""
    polymer, rules, charcounts = parse_input(lines)

    if DEBUG:
        print(polymer)
        print(rules)
        print(charcounts)

    for i in range(steps):
        # print(f"--- Step {i} --")
        new_pairs = defaultdict(int)

        for pair, ins in rules.items():
            cnt = polymer[pair]
            if cnt > 0:
                new_pairs[pair[0] + ins] += cnt
                new_pairs[ins + pair[1]] += cnt
                charcounts[ins] += cnt
                polymer[pair] = 0

        for new_pair, cnt in new_pairs.items():
            polymer[new_pair] += cnt

        # print(polymer)

    # print(charcounts)
    # sorted_counts = sorted(charcounts.items(), key=lambda x: x[1])

    counts = sorted(charcounts.values())
    # print("Total length", sum(counts))

    return counts[-1] - counts[0]


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 40)


tests = [
    (utils.load_input('test.1.txt'), 1749 - 161, 2192039569602-3849876073),
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
    exp1 = 2768
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 2914365137499
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
