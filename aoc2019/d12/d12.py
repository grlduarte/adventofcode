'''
gduarte@astro.ufsc.br
Created on 02-mai-2020
'''

from itertools import permutations

class Vector(tuple):
    '''
    Creates a subclass to treat tuples as if they were vectors.
    Calling len(Vector) should return its associated energy, i.e.
    the sum of the absolute value of its components.
    '''
    def __new__(cls, x, y, z=0):
        return super().__new__(cls, (x, y, z))

    
    def __init__(self, x, y, z):
        self.x = self[0]
        self.y = self[1]
        self.z = self[2]

    
    def __len__(self):
        return sum(abs(_) for _ in self)


    def __add__(self, value):
        x = self[0] + value[0]
        y = self[1] + value[1]
        z = self[2] + value[2]
        return Vector(x, y, z)


    def __sub__(self, value):
        x = self[0] - value[0]
        y = self[1] - value[1]
        z = self[2] - value[2]
        return Vector(x, y, z)


class Moon:
    def __init__(self, init_pos):
        init_pos
        self.r = Vector(*init_pos)
        self.v = Vector(0, 0, 0)
        self.energy = len(self.r) * len(self.v)


    def __repr__(self):
        return f"<pos={self.r}, vel={self.v}>"


    def update_velocity(self, another_moon):
        for i in range(3):
            dv = [0, 0, 0]
            dv[i] = 1
            dv = Vector(*dv)
            if self.r[i] < another_moon.r[i]:
                self.v += dv
            elif self.r[i] > another_moon.r[i]:
                self.v -= dv


    def update_position(self):
        self.r += self.v
        self.energy = len(self.r) * len(self.v)


class MoonsSystem(list):
    def __init__(self, positions_file):
        self._read_input(positions_file)
        self.set_initial_state()


    def _read_input(self, fname):
        def input_to_tuple(pos):
            replace_char = ['<', '>', 'x=', 'y=', 'z=']
            for char in replace_char:
                pos = pos.strip().replace(char, '')
            pos = pos.split(',')
            pos = [int(p) for p in pos]
            return tuple(pos)

        with open(fname, 'r') as f:
            positions = f.readlines()
        self.init_pos = [input_to_tuple(pos) for pos in positions]


    def set_initial_state(self):
        super().__init__([Moon(pos) for pos in self.init_pos])
        self.system_energy = sum(m.energy for m in self)


    def time_step(self):
        for i,j in permutations(range(len(self)), 2):
            self[i].update_velocity(self[j])
    
        self.system_energy = 0
        for moon in self:
            moon.update_position()
            self.system_energy += moon.energy


def get_periods(moons):
    def bool_prod(bool_dict):
        result = True
        for key in bool_dict:
            for element in bool_dict[key]:
                result = (result and element)
        return result
    
    axes = dict()
    for i in range(3):
        axes[i] = [[(moon.r, moon.v)] for moon in moons]

    done = {0: [False, False, False, False],
            1: [False, False, False, False], 
            2: [False, False, False, False]} 

    while not bool_prod(done):
        moons.time_step()
        for i in range(3):
            for j,moon in enumerate(moons):
                if not done[i][j]:
                    axes[i][j].append((moon.r[i], moon.v[i]))
                    if (axes[i][j][-1] in axes[i][j][:-1]):
                        done[i][j] = True

    return axes, done


def part_one():
    moons = MoonsSystem('input.dat')

    step = 0
    while step < 1000:
        moons.time_step()
        step += 1
    return moons.system_energy


def part_two():
    moons = MoonsSystem('input.dat')

'''
for axis in axes:
    print(f'axis {axis}:')
    for i,element in enumerate(axes[axis]):
        print(f'  moon {i} :: {len(element)-1} - {element.index(element[-1])} = ', end='')
        print(f'{len(element)-1 - element.index(element[-1])} :: ', end='')
        print(f' {element[element.index(element[-1])]} {element[-1]}')
'''
