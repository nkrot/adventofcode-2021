#!/usr/bin/env python

# # #
#
#

import os
import sys
from typing import List, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DAY = '20'
DEBUG = int(os.environ.get('DEBUG', 0))


class ImageEnhancementAlgorithm(object):

    def __init__(self, data: str):
        self.data = list(data)

    def show_table(self):
        """conversion table"""
        for idx, ch in enumerate(self.data):
            bn = f"{idx:0>9b}"
            s = "".join(["#" if int(n) % 2 else "." for n in list(bn)])
            print("{}: {} {} --> {}".format(idx, bn, s, ch))

    # TODO: this method is called crazy amount of times. optimize it?
    def recode(self, seq: Union[str, List[Union['Pixel', int]]]) -> str:
        """Given a stride of a pixel, return new pixel value that results
        from the stride according to the algorithm.
        """
        if isinstance(seq, str):
            ints = [Pixel.VALUES[ch] for ch in list(seq)]
        else:
            ints = [int(p) for p in seq]
        binary_string = "".join(str(i) for i in ints)
        dec = int(binary_string, 2)
        return self.data[dec]

    def enhance(self, image: 'Image'):
        """Enhance given image once, modifying it in place"""

        if DEBUG > 1:
            print("--- enhancing ---")

        # After one round of image enhancement, the image will grow in size
        # one pixel on each side. Here we prepare the image for that by adding
        # a padding of size 1.
        image.pad(image.outside_pixel)

        # compute new pixel values but do not update the pixels themselves
        new_pixel_values = []
        for pos, pixel in image:
            stride = image.get_stride(pos)
            new_value = self.recode(stride)
            if pixel.value != new_value:
                new_pixel_values.append((pixel, new_value))

        # update pixel values
        for pixel, new_value in new_pixel_values:
            pixel.value = new_value

        # update outside pixel (InfinitePixel)
        image.outside_pixel = next(image.outside_pixel)

        if DEBUG > 1:
            print("Number of updated pixels", len(new_pixel_values))
            image.inspect("Enhanced image")


class Pixel(object):

    VALUES = {'.': 0, '#': 1}

    def __init__(self, value: Union[str, 'Pixel'] = '.'):
        self.value = str(value)

    def __int__(self):
        return self.VALUES[self.value]

    # removed to improve runtime speed
    # def __eq__(self, other: Union[int, str, 'Pixel']):
    #     if isinstance(other, (str, int)):
    #         return type(other)(self) == other
    #     elif isinstance(other, type(self)):
    #         return str(self) == str(other)
    #     raise Exception("Non-comparable type: {}".format(type(other)))

    # removed to improve runtime speed
    # def __ne__(self, other):
    #     return not(self.__eq__(other))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "<{}: value={}>".format(self.__class__.__name__, self.value)


class InfinityPixel(Pixel):
    """A special kind of pixel that knows how it should change in the next step"""

    def __init__(self, initial_value, changer):
        super().__init__(initial_value)
        self.changer = changer

    def __next__(self):
        """Return next state of the pixel that is surrounded by pixels of same
        kind, like a dark pixel surrounded by dark pixels or a light pixel
        surrounded by light pixels."""
        stride = [int(self)] * 9
        new_value = self.changer.recode(stride)
        return self.__class__(new_value, self.changer)


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
        self.outside_pixel = None
        self._set_spans()
        # self._strides = {}

    def __iter__(self):
        pixels = list(self.pixels.items())
        return iter(pixels)

    def __len__(self):
        return len(self.pixels)

    def _set_spans(self):
        """Sets self.xspan and self.yspan variables"""
        xs, ys = set(), set()
        for (x, y) in self.pixels:
            xs.add(x)
            ys.add(y)
        xs = sorted(xs)
        ys = sorted(ys)
        self.xspan = [xs[0], xs[-1]]
        self.yspan = [ys[0], ys[-1]]

    # def get_stride2(self, xy) -> List[Pixel]:
    #     """Return pixels in the 3x3 window around the position <xy>.
    #     This method maintains a cache of answers of the form
    #       strides[xy] = [(x1, y1), (x2,y2), ..., (x9, y9)]
    #     It turns out that this approach makes performance worse.
    #     """
    #     if xy not in self._strides:
    #         x, y = xy
    #         self._strides[xy] = [(x+dx, y+dy) for dx, dy in self.STRIDE]
    #     stride = [self.pixels.get(_xy, self.outside_pixel)
    #                 for _xy in self._strides[xy]]
    #     return stride

    def get_stride(self, xy) -> List[Pixel]:
        """Return pixels in the 3x3 window around the position <xy>"""
        x, y = xy
        stride = [0] * 9
        for idx, (dx, dy) in enumerate(self.STRIDE):
            xy = x+dx, y+dy
            stride[idx] = self.pixels.get(xy, self.outside_pixel)
        return stride

    def pad(self, value: Union[str, 'Pixel'] = '.'):
        """Add padding along the borders (outside) of the current image"""
        self.xspan = [self.xspan[0]-1, self.xspan[1]+1]
        self.yspan = [self.yspan[0]-1, self.yspan[1]+1]
        minx, maxx = self.xspan
        miny, maxy = self.yspan
        for x in (minx, maxx):
            for y in range(miny, maxy+1):
                self.pixels[(x,y)] = Pixel(value)
        for y in (miny, maxy):
            for x in range(minx, maxx+1):
                self.pixels[(x,y)] = Pixel(value)

    def count_lit_pixels(self):
        return sum(int(pix) for pix in self.pixels.values())

    def shape(self):
        xdim = 1 + self.xspan[1] - self.xspan[0]
        ydim = 1 + self.yspan[1] - self.yspan[0]
        return (xdim, ydim)

    def __str__(self):
        minx, maxx = self.xspan
        miny, maxy = self.xspan
        out = ''
        for x in range(minx, maxx+1):
            for y in range(miny, maxy+1):
                xy = (x, y)
                pixel = self.pixels.get(xy, xy)
                out += str(pixel)
            out += '\n'
        return out

    def inspect(self, title='Image'):
        print(f"--- {title} ---")
        print("Image shape: {}, Number of lit pixels: {}".format(
            self.shape(), self.count_lit_pixels()))
        print("Outside pixel:", repr(self.outside_pixel))
        print(str(self))


def test_iea_1():
    data = utils.load_input("test.1.txt")[0]
    # data = utils.load_input("input.txt")[0]
    algo = ImageEnhancementAlgorithm(data)
    algo.show_table()


def test_iea_2():
    data = utils.load_input("test.1.txt")[0]
    algo = ImageEnhancementAlgorithm(data)
    tests = [(".........", ".")]
    for input, exp in tests:
        res = algo.recode(input)
        print(exp == res, exp, res)
        pixels = [Pixel(ch) for ch in input]
        res = algo.recode(pixels)
        print(exp == res, exp, res)


def test_pixel():
    tests = [
            (Pixel('.'), 0, "."),
            (Pixel('#'), 1, "#")
            ]
    for pix, num, string in tests:
        print("exists?", bool(pix))
        print("numeric value?", num == int(pix), num, int(pix))
        print("string value?", string == str(pix), string, str(pix))
        # corresponding methods __eq__ and __ne__ were removed to improve runtime
        # print("Equal to number?", pix == num)
        # print("Equal to number?", num == pix)
        # print("Non-Equal to number?", pix != 2)
        # print("Non-Equal to number?", 2 != pix)
        # print("Equal to string?", pix == string)
        # print("Equal to string?", string == pix)
        # print("Non-Equal to string?", pix != 'x')
        # print("Non-Equal to string?", 'x' != pix)
    pix1, pix2 = tests[0][0], tests[1][0]
    print(pix1 == pix1)
    print(pix1 != pix2)


def test_infinity_pixel():
    data = utils.load_input("input.txt")[0]
    algo = ImageEnhancementAlgorithm(data)
    pixel = InfinityPixel(".", algo)
    exp = [".", "#", ".", "#", ".", "#"]
    pixels = [pixel]
    for _ in range(5):
        pixel = next(pixel)
        pixels.append(pixel)
    res = list(map(str, pixels))
    print(exp == res, exp, res)


# test_iea_1()
# test_iea_2()
# test_pixel()
# test_infinity_pixel()
# exit(100)


def parse_input(lines: List[str]):
    algo = ImageEnhancementAlgorithm(lines[0])
    image = Image.from_lines(lines[2:])
    return algo, image


def solve_p1(lines: List[str], times=2) -> int:
    """Solution to the 1st part of the challenge"""
    algo, image = parse_input(lines)
    image.outside_pixel = InfinityPixel(".", algo)

    if DEBUG:
        image.inspect("Initial image")

    for t in range(times):
        algo.enhance(image)

    if DEBUG:
        image.inspect(f"Final image, enhanced {times} times")

    return image.count_lit_pixels()


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 50)


tests = [
   (utils.load_input('test.1.txt'), 35, 3351),
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
    exp1 = 4873
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 16394
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


def main():
    run_tests()
    run_real()


if __name__ == '__main__':
    main()