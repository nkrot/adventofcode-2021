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

DAY = '20'
DEBUG = int(os.environ.get('DEBUG', 0))


class Pixel(object):

    VALUES = {".": 0, "#": 1}

    def __init__(self, value: str = "."):
        self.value = str(value)

    def __int__(self):
        return self.VALUES[self.value]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "<{}: value={}>".format(self.__class__.__name__, self.value)


class Image(object):

    STRIDE = [(-1, -1), (-1, 0), (-1, +1),
              (0,  -1), (0,  0), (0,  +1),
              (+1, -1), (+1, 0), (+1, +1)]

    @classmethod
    def from_lines(cls, lines: List[str]):
        pixels = {}
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                pixels[(x,y)] = Pixel(char)
        return cls(pixels)

    def __init__(self, pixels):
        self.pixels = pixels
        self.padding = {}

    def __iter__(self):
        pixels = list(self.pixels.items())
        pixels.extend(list(self.padding.items()))
        return iter(pixels)

    def __len__(self):
        return len(self.pixels)

    def get_stride(self, xy) -> List[Pixel]:
        """create if necessary"""
        x, y = xy
        stride = []
        for dx, dy in self.STRIDE:
            xy = x+dx, y+dy
            pixel = self.pixels.get(xy, self.padding.get(xy, Pixel()))
            stride.append(pixel)
        return stride

    def pad(self, value='.'):
        """Add temporary padding (should be removed with .unpad())"""
        self.padding = {}
        xs, ys = self.xs(), self.ys()
        minx, maxx = xs[0]-1, xs[-1]+1
        miny, maxy = ys[0]-1, ys[-1]+1
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                xy = (x,y)
                if xy not in self.pixels:
                    pix = Pixel(value)
                    # self.pixels[xy] = pix # did not work
                    self.padding[xy] = pix

    def extend(self, value='.'):
        """Add padding immediately"""
        self.pad(value)
        for xy, pixel in self.padding.items():
            self.pixels[xy] = pixel
        self.padding = {}

    def unpad(self):
        """Keep padding that has light pixels and remove padding consisting of
        all dark pixels only"""
        for xy, pixel in self.padding.items():
            if int(pixel) == 1:
                assert xy not in self.pixels, "Oh shit"
                self.pixels[xy] = pixel
        self.padding = {}
        # adjust the shape of the image to rectangle
        for x in self.xs():
            for y in self.ys():
                xy = (x, y)
                if xy not in self.pixels:
                    self.pixels[xy] = Pixel()

    def num_lit_pixels(self):
        return sum(int(pix) for pix in self.pixels.values())

    def shape(self):
        return (len(self.xs()), len(self.ys()))

    def xs(self):
        xs = set()
        xys = list(self.pixels.keys()) + list(self.padding.keys())
        for xy in xys:
            xs.add(xy[0])
        return sorted(xs)

    def ys(self):
        ys = set()
        xys = list(self.pixels.keys()) + list(self.padding.keys())
        for xy in xys:
            ys.add(xy[1])
        return sorted(ys)

    def __str__(self):
        xs, ys = self.xs(), self.ys()
        out = ''
        for x in self.xs():
            for y in self.ys():
                xy = (x, y)
                pixel = self.pixels.get(xy, self.padding.get(xy))
                out += str(pixel)
            out += '\n'
        return out


def parse_input(lines: List[str]):
    algo = lines.pop(0)
    return algo, Image.from_lines(lines[1:])


# What happens to pixels in the infinity
# 1) a . that is completely surrounded by . turn to # (ON)
# 2) a # that is completely surrounded by # turns to . (OFF)
# With number of iterations being even, inifinity is all OFF (.)
# but what happens in the proximity of the image?


def enhance(image, algo, step):
    print("--- enhancing ---")
    char = '.'
    #char = '#' if step % 2 else '.'
    #print("Padding with ", char)
    image.pad(char)
    print("Initial image {}\n{}".format(image.shape(), image))
    new_pixel_values = []
    # compute new pixel values
    for pos, pixel in image:
        # print(pos, pixel)
        stride = image.get_stride(pos)
        # print("", "".join([str(p) for p in stride]))
        binseq = "".join([str(int(pix)) for pix in stride])
        dec = int(binseq, 2)
        new_value = algo[dec]
        # print(binseq, dec, new_value)
        if pixel.value != new_value:
            new_pixel_values.append((pixel, new_value))
    # update pixel values
    print("Number of pixels to update", len(new_pixel_values))
    for pixel, value in new_pixel_values:
        pixel.value = value
    image.unpad()
    print("Resulting image {}\n{}".format(image.shape(), image))


def solve_p1(lines: List[str], times=2) -> int:
    """Solution to the 1st part of the challenge"""
    algo, image = parse_input(lines)
    print(image.shape(), image.num_lit_pixels())
    for t in range(times):
        enhance(image, algo, t)
        print("Number of lit pixels", image.num_lit_pixels())
    return image.num_lit_pixels()


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
   (utils.load_input('test.1.txt'), 35, None),
    # (utils.load_input('test.2.txt'), -43, None),

    # After one iteration:
    # test.3.txt shows that a . surrounded all by . turns to #
    # (utils.load_input('test.3.txt'), -43, None),

    # test.4.txt shows that a # surrounded all by # turn to .
    # check the central 3x3 area!
    #(utils.load_input('test.4.txt'), -43, None),
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
    exp1 = -4525  # too low
    exp1 = -4846  # too low
    exp1 = -4942  # too high
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
#    run_real()
