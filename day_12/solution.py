#!/usr/bin/env python

# # #
# TODO: improve speed in p.2
# + do not use exceptions? -- saves 1 second
# + use deque instead of mere list -- saves 5 seconds
# + count paths directly instead of accumulating and then counting -- saves <1 s
# - rethink checking for visited small caves. counting them seems to be taking lot of time

import re
import os
import sys
from typing import List, Dict
from collections import defaultdict, Counter, deque

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '12'
DEBUG = False


def build_graph(lines: List[str]) -> Dict[str, List[str]]:
    graph = defaultdict(set)
    for line in lines:
        if line:
            src, trg = line.split('-')
            graph[src].add(trg)
            graph[trg].add(src)
    # print(graph)
    return graph


class GraphPathException(Exception):
    """raised if path is incorrect"""


class GPath(object):
    """A path through the graph as a list of nodes"""

    def __init__(self, src = None):
        self.nodes = []
        if isinstance(src, list):
            self.nodes = src
        elif isinstance(src, str):
            self.nodes.append(src)

    def _can_be_added(self, newnode) -> bool:
        if newnode.islower() and newnode in self.nodes:
            return False
        return True

    def is_full(self):
        return self.last == 'end'

    def __add__(self, node):
        # if not self._can_be_added(node):
        #     raise GraphPathException(f"Cannot add node {node} to path")
        return self.__class__(self.nodes + [node])

    def __str__(self):
        return ",".join(self.nodes)

    @property
    def last(self):
        return self.nodes[-1]


class GPath2(GPath):

    def __init__(self, *args):
        super().__init__(*args)
        self.counts = defaultdict(int)
        self.most_visits = 0

    def _count_small_nodes(self):
        self.counts = Counter([n for n in self.nodes if n.islower()])
        most_visited = self.counts.most_common(1)
        if most_visited:
            self.most_visits = most_visited[0][1]

    def _can_be_added(self, node: str) -> bool:
        if node.islower() and node in self.nodes:
            if node in {'start', 'end'}:
                # can be visited only once
                return False
            if not self.counts:
                self._count_small_nodes()
            if self.most_visits > 1:
                # We are allowed to visit twice one small node only and there
                # is already a small node that has already been visited twice.
                return False
        return True


def count_paths(graph, PathClass) -> int:

    paths = deque([PathClass("start")])
    full_paths = []
    c_full_paths = 0

    # BFS to build all paths between <start> and <end> nodes
    while paths:
        path = paths.popleft()
        for trg in graph[path.last]:
            if path._can_be_added(trg):
                newpath = path + trg
                if newpath.is_full():
                    # full_paths.append(newpath)
                    c_full_paths += 1
                else:
                    paths.append(newpath)
            # except GraphPathException:
            #     # print("Oh shit", path, trg)
            #     pass

    # if DEBUG:
    #     print("--- Full paths ---")
    #     for p in full_paths:
    #         print(p)

    return c_full_paths


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    return count_paths(build_graph(lines), GPath)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return count_paths(build_graph(lines), GPath2)


tests = [
    (utils.load_input('test.1.txt'), 10, 36),
    (utils.load_input('test.2.txt'), 19, 103),
    (utils.load_input('test.3.txt'), 226, 3509),
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
    exp1 = 4691
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 140718
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
