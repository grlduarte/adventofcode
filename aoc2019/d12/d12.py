'''
gduarte@astro.ufsc.br
Created on 02-mai-2020
'''

#FIXME: part 2 not working

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

    def calc_energy(self):
        return len(self.r) * len(self.v)


class MoonsSystem(list):
    def __init__(self, positions_file):
        self._read_input(positions_file)
        self.t = 0
        super().__init__([Moon(pos) for pos in self.init_pos])

    def __repr__(self):
        out = ""
        for moon in self:
            out += repr(moon) + "\n"
        return out

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

    def time_step(self):
        for i,j in permutations(range(len(self)), 2):
            self[i].update_velocity(self[j])
        for moon in self:
            moon.update_position()
        self.t += 1

    def calc_energy(self):
        energy = 0
        for moon in self:
            energy += moon.calc_energy()
        return energy


def gcd(x, y):
    return y if x==0 else gcd(y%x, x)


def lcm(x, y):
    return x*y // gcd(x, y)


def get_periods(moons):
    p = [False, False, False]
    ax = {0: [], 1: [], 2: []}
            
    while True:
        for i in range(3):
            s = (tuple(moon.r[i] for moon in moons),
                 tuple(moon.v[i] for moon in moons))
            if (s in ax[i]) and (not p[i]):
                p[i] = len(set(ax[i]))
                print(p)
            ax[i].append(s)
        if all(p):
            break
        moons.time_step()
    period = lcm(lcm(p[0], p[1]), p[2])
    return period


def part_one():
    moons = MoonsSystem('input.dat')

    step = 0
    while step < 1000:
        moons.time_step()
        step += 1
    return moons.calc_energy()


def part_two():
    moons = MoonsSystem('input.dat')
    # sit and relax
    p = get_periods(moons)
    return p
