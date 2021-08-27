'''
gduarte@home-vm
Created on 27-ago-2021
'''

from computer import Computer


def part_one():
    comp = Computer('input.dat', mem_alloc=4096, screen_size=64)
    comp.run()
    count = 0
    for tile in comp.screen:
        if (tile == 2): count += 1
    return count


def part_two()
    comp = Computer('input.dat', mem_alloc=4096, screen_size=64)
    comp.memory[0] = 2
    comp.run()


if __name__ == "__main__":
    print(part_one())
