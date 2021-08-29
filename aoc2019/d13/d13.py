'''
gduarte@home-vm
Created on 27-ago-2021
'''

import numpy as np

from computer import Computer


def part_one(comp):
    x, y = [23, 45]
    screen = np.array([[0 for _ in range(y)] for _ in range(x)])
    while (comp.status != 'halt'):
        comp.cycle()
        try:
            x, y, v = comp.output
            comp.output = []
            screen[y, x] = v
        except ValueError:
            continue
    count = 0
    for line in screen:
        for px in line:
            if (px == 2): count += 1
    return count, screen


def part_two(comp, screen):
    comp.reset()
    score = 0
    comp.memory[0] = 2
    while (comp.status != 'halt'):
        try:
            x_ball = np.where(screen == 4)[1][0]
            x_pad = np.where(screen == 3)[1][0]
        except IndexError:
            x_ball = 0
            x_pad = 0
        if (x_ball > x_pad):
            signal = 1
        elif (x_ball < x_pad):
            signal = -1
        else:
            signal = 0

        comp.cycle(signal)
        try:
            x, y, v = comp.output
            comp.output = []
            if (x < 0) and (y == 0):
                score = v
                continue
            else:
                screen[y, x] = v
        except ValueError:
            continue
    return score


if __name__ == "__main__":
    comp = Computer('input.dat', mem_alloc=4096)
    count, screen = part_one(comp)
    print(count)
    print(part_two(comp, screen))
