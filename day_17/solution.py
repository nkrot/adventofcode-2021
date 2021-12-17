#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '17'
DEBUG = False


class TargetArea(object):

    @classmethod
    def from_text(cls, line: str):
        m = re.search(r'x=(-?\d+)\.+(-?\d+), y=(-?\d+)\.+(-?\d+)', line)
        assert m, f"Failed to parse: {line}"
        xspan = (int(m[1]), int(m[2]))
        yspan = (int(m[3]), int(m[4]))
        return cls(xspan, yspan)

    def __init__(self, xspan, yspan):
        self.xspan = sorted(xspan)
        self.yspan = sorted(yspan)

    def __contains__(self, point) -> bool:
        x, y = point.xy if isinstance(point, Probe) else point
        return (self.xspan[0] <= x <= self.xspan[1] 
                and self.yspan[0] <= y <= self.yspan[1])

    @property
    def tl(self):
        """top left corner"""
        return (self.xspan[0], self.yspan[1])

    @property
    def br(self):
        """bottom right corner"""
        return (self.xspan[1], self.yspan[0])
        
    @property
    def lower_y(self):
        return min(self.yspan)


class Probe(object):

    def __init__(self, vx, vy):
        self.x, self.y = (0, 0)
        self.vx = int(vx)  # horizontal velocity
        self.vy = int(vy)  # vertical velocity
        self.maxy = 0   # maximum altitude reached by the probe
        self.time = 0

    @property
    def max_altitude(self):
        return self.maxy

    @property
    def xy(self):
        return (self.x, self.y)

    def move(self):
        """one step in time"""
        self.time += 1
        self.x += self.vx
        self.y += self.vy
        # drag affects horizontal velocity
        if self.vx > 0:
            self.vx -= 1
        elif self.vx < 0:
            self.vx += 1
        # gravity affects vertical velocity
        self.vy -= 1
        if self.y > self.maxy:
            self.maxy = self.y

    def __repr__(self):
        return "<{}: position={}, velocity={}, time={}, maxy={}>".format(
            self.__class__.__name__, (self.x, self.y), (self.vx, self.vy),
            self.time, self.maxy)


def test_target_area():
    line = utils.load_input('test.1.txt')[0]
    area = TargetArea.from_text(line)

    hits = [(21,-9), (20, -9),
            (20, -10), (20, -5), (30, -10), (30, -5)]
    for loc in hits:
        assert loc in area, f"Must be inside: {loc}"
    
    misses = [(20, -4), (20, -11)]
    for loc in misses:
        assert loc not in area, f"Must be outside: {loc}"


# test_target_area()

def launch(probe: Probe, target_area: TargetArea) -> bool:
    if DEBUG:
        print("--- Launching ---")
        print(probe)
    success = False
    while True:
        probe.move()
        success = probe in target_area
        if DEBUG:
            print(probe, success)
        if success or probe.y < target_area.lower_y:
            break
    if DEBUG:
        print("Success?", success)
    return success


# TODO: there must be a better method of computing velocities
def velocities_1(area):
    # for now just brute force solution
    maxx, _ = area.tl
    for vx in range(0, area.tl[0]):
        for vy in range(1, maxx-vx):
            yield vx, vy


def velocities_2(area):
    # some examples from the task that relate to test.1.txt
    # for vx, vy in [(14,-2), (30,-9), (9,-2)]:
    #     yield vx, vy

    # for now just brute force solution
    maxx, miny = area.br
    for vx in range(0, 1+maxx):
        for vy in range(miny, 100):
            yield vx, vy


def run_simulations(area, velocities) -> Tuple[Probe, int]:
    best = None
    c_successful_probes = 0
    for vx, vy in velocities():
        probe = Probe(vx, vy)
        success = launch(probe, area)
        if success:
            c_successful_probes += 1
            # print("Success? {} with initial velocity {} reaches max altitude {}:".format(
            #     success, (vx,vy), probe.max_altitude))
            if not best or best.max_altitude < probe.max_altitude:
                best = probe
    # print("Total successful probes", c_successful_probes)
    return best, c_successful_probes


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    area = TargetArea.from_text(lines[0])
    best, _ = run_simulations(area, lambda: velocities_1(area))
    return best.max_altitude


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    area = TargetArea.from_text(lines[0])
    _, total_successes = run_simulations(area, lambda: velocities_2(area))
    return total_successes


tests = [
    (utils.load_input('test.1.txt'), 45, 112),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T.{tid}.p1:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T.{tid}.p2:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 4095
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 3773
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
