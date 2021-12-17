#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Generator

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '17'
DEBUG = int(os.environ.get('DEBUG', 0))
T_VELOCIY = Tuple[int, int]  # x-velocity, y-velocity


class TargetArea(object):

    @classmethod
    def from_text(cls, line: str):
        m = re.search(r'x=(-?\d+)\.+(-?\d+), y=(-?\d+)\.+(-?\d+)', line)
        assert m, f"Failed to parse: {line}"
        xspan = (int(m[1]), int(m[2]))
        yspan = (int(m[3]), int(m[4]))
        # an alternative to get all numbers from the line
        # numbers = list(map(int, filter(len, re.split('[^\d-]+', line))))
        return cls(xspan, yspan)

    def __init__(self, xspan, yspan):
        self.xspan = sorted(xspan)
        self.yspan = sorted(yspan)

    def __contains__(self, point) -> bool:
        x, y = point.xy if isinstance(point, Probe) else point
        return (self.xspan[0] <= x <= self.xspan[1]
                and self.yspan[0] <= y <= self.yspan[1])

    @property
    def lower_y(self):
        return self.yspan[0]


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
    """Launch give probe and move it until it is clear whether it hit given
    <target_area> or overshot. Return True if the probe hit the target area,
    otehrwise return False.
    """
    if DEBUG > 2:
        print("--- Launching ---")
        print(probe)
    success = False
    while True:
        probe.move()
        success = probe in target_area
        if DEBUG > 2:
            print(probe, success)
        if success or probe.y < target_area.lower_y:
            break
    if DEBUG > 2:
        print("Success?", success)
    return success


def get_vx_range(area) -> Tuple[int, int]:
    """Find minimal and maximal horizontal speeds that make sense, such that
    a) min speed is sufficient to reach the left edge of the target area
    b) max speed does not lead to overshooting (not always the best speed)
    """
    closest, farthest = area.xspan
    min_vx, max_vx = 0, farthest
    for vx in range(min_vx, 1+max_vx):
        reach = sum(range(1, 1+vx))
        if reach >= closest:
            min_vx = vx
            break
    return (min_vx, max_vx)


def velocities_p1_1(area) -> Generator[T_VELOCIY, None, None]:
    """Generate possible initial velocity parameters for the probes in part 1.
    """
    closest_x, farthest_x = area.xspan
    min_vx, max_vx = get_vx_range(area)
    # max_vx can be lower than the one computed above. The one computed
    # above is for the case when the probe reaches the target area in *one*
    # step with vertical speed being equal to 0. This is not true for part 1
    # because in part 1 the probe needs to *climb* to reach max altitude.
    # Therefore:
    max_vx = farthest_x // 2
    for vx in range(min_vx, max_vx):
        max_vy = closest_x - vx  # TODO: just guessing. explain?
        for vy in range(1, max_vy):
            yield vx, vy


def velocities_p2_1(area) -> Generator[T_VELOCIY, None, None]:
    """Generate possible initial velocity parameters for the probes in part 2.
    """
    closest_x, farthest_x = area.xspan
    min_vx, max_vx = get_vx_range(area)

    # case 1: points in area that can be reached in more than one step
    max_vx = (1 + farthest_x) // 2  # anything larger will x-overshoot at any
                                    # step larger than 2.
    min_vy = 1 + area.lower_y // 2  # anything larger will y-overshoot (be
                                    # below the lowest side of the target area)
                                    # at any step large than 2
    max_vy = closest_x  # TODO: actually, lower
    if DEBUG > 1:
        print("Velocity range hor [{},{}] and vert [{},{}]".format(
            min_vx, max_vx, min_vy, max_vy))
    for vx in range(min_vx, max_vx+1):
        for vy in range(min_vy, max_vy+1):
            yield vx, vy

    # case 2: points in the target area can be reached within one step:
    # velocities are simply coordinates of the points.
    min_vx, max_vx = area.xspan
    min_vy, max_vy = area.yspan
    if DEBUG > 1:
        print("Velocity range hor [{},{}] and vert [{},{}]".format(
            min_vx, max_vx, min_vy, max_vy))
    for vx in range(min_vx, max_vx+1):
        for vy in range(min_vy, max_vy+1):
            yield vx, vy


@utils.mytimeit
def run_simulations(area, velocities) -> Tuple[Probe, int]:
    """Lauch probes for each of the initial velocities from <velocities> and
    return best probe (for part 1) as well as the total number of probes that
    reached the target area (part 2).
    """
    best = None
    c_probes = 0
    c_successful_probes = 0
    for vx, vy in velocities():
        c_probes += 1
        probe = Probe(vx, vy)
        success = launch(probe, area)
        if success:
            c_successful_probes += 1
            if DEBUG > 1:
                print("Success: initial velocity {} --> max altitude {}".format(
                    (vx,vy), probe.max_altitude))
            if not best or best.max_altitude < probe.max_altitude:
                best = probe
    if DEBUG > 0:
        print("Probes total/successful: {}/{}".format(
            c_probes, c_successful_probes))
    return best, c_successful_probes


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    area = TargetArea.from_text(lines[0])
    best, _ = run_simulations(area, lambda: velocities_p1_1(area))
    return best.max_altitude


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    area = TargetArea.from_text(lines[0])
    _, total_successes = run_simulations(area, lambda: velocities_p2_1(area))
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
