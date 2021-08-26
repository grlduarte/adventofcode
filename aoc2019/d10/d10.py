'''
gduarte@astro.ufsc.br
Created on 30-Apr-2020
'''

#TODO: needs urgent refactoring

from itertools import product
from math import gcd


class AsteroidsMap:
    def __init__(self, input_file: str):
        self.input_file = input_file
        with open(self.input_file, 'r') as f:
            asteroids = f.readlines()
        self.map = [ list(row.strip()) for row in asteroids ]


    def find_sweet_spot(self):
        x_range = len(self.map[0])
        y_range = len(self.map)
        counts = {}

        for x,y in product( range(x_range), range(y_range) ):
            if self.map[y][x] == '#':
                count = 0
                for los in LineOfSight(x, y, x_range, y_range):
                    if '#' in [ self.map[c[1]][c[0]] for c in los ]:
                        count+=1
                counts.update( {(x,y) : count} )

        coords = max(counts, key=counts.get)

        return(coords, counts[coords])


    def blast_em_all(self, IMS_coords: tuple, n_blast: int = 200):
        x_range = len(self.map[0])
        y_range = len(self.map)
        vaporized = 0

        #FIXME: if the total number of asteroids is less than
        #       n_blast the loop is infinite
        while vaporized < n_blast:
            for los in LineOfSight(*IMS_coords, x_range, y_range):
                if vaporized < n_blast:
                    for c in los:
                        if self.map[c[1]][c[0]] == '#':
                            self.map[c[1]][c[0]] = '.'
                            vaporized += 1
                            break
                else: break

        return c


class LineOfSight:
    def __init__(self, x_center, y_center, x_range, y_range):
        self.x_center = x_center
        self.y_center = y_center
        self.x_range  = x_range
        self.y_range  = y_range
        self._set_directions()
        self.i = 0


    def _set_directions(self):
        cos = lambda c: c[1] / ( c[0]**2 + c[1]**2 )**(1/2)

        ## First semicircle
        semicircle = set()
        for dx,dy in product( range(self.x_range-self.x_center), range(self.y_range) ):
            dy -= self.y_center
            div = gcd(dx, dy)
            if (dx == 0) and (dy == 0):
                pass
            else:
                dx //= div
                dy //= div
                semicircle.add( (dx,dy) )
        d1 = sorted( list(semicircle), key=cos)

        ## Second semicircle
        semicircle = set()
        for dx,dy in product( range(self.x_center), range(self.y_range) ):
            dx -= self.x_center
            dy -= self.y_center
            div = gcd(dx, dy)
            if (dx ==0) and (dy == 0):
                pass
            else:
                dx //= div
                dy //= div
                semicircle.add( (dx,dy) )
        d2 = sorted( list(semicircle), key=cos, reverse=True)

        self.directions = d1 + d2


    def __iter__(self):
        return self


    def __next__(self):
        try:
            dx,dy = self.directions[self.i]
        except IndexError:
            raise StopIteration

        los = []

        step = 1
        x = self.x_center + step*dx
        y = self.y_center + step*dy

        los.append( (x,y) )
        step += 1
        x = self.x_center + step*dx
        y = self.y_center + step*dy

        while (x >= 0) and (y >= 0) and (x < self.x_range) and (y < self.y_range):
            los.append( (x,y) )
            step += 1
            x = self.x_center + step*dx
            y = self.y_center + step*dy

        self.i += 1
        return los


if __name__ == '__main__':
    ast = AsteroidsMap('input.dat')
    sweet_spot, visible = ast.find_sweet_spot()
    print("Part one: %d" % visible)
    last_blast = ast.blast_em_all(sweet_spot)
    print("Part two: %d" % (last_blast[0]*100+last_blast[1]) )
