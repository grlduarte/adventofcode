'''
gduarte@astro.ufsc.br
Created on 18-abr-2020
'''

class UniversalOrbitMap:
    def __init__(self, input_map):
        with open(input_map, 'r') as f:
            self._read_file(f)
        self._calc_checksum()
        

    def _read_file(self, f):
        '''
        The attribute orbits is a dictionary that tells all
        the orbits read in the orbit map. For example,
            
            >> self.orbits['flying_saucer']

        tells you the object the  flying saucer is directly
        orbitting.
        '''

        self.orbits = {}
        for line in f.readlines():
            orbited, orbiting = line.strip().split(')')
            self.orbits.update( {orbiting : orbited} )


    def _calc_checksum(self):
        '''
        Sums all the direct and indirect orbit count to get
        the checksum.
        '''
        self.checksum = 0
        for obj in self.orbits.keys():
            self.checksum += len( self.get_orbit(obj) )


    def get_orbit(self, obj: str):
        '''
        Returns  all the objects orbited directly and indi-
        rectly by obj.
        '''
        orbit = []
        while True:
            ## It's easier to ask for forgiveness than permission (EAFP)
            ##
            ## Assumes all keys exists in self.orbits and raises an exception
            ## when that's not true. That's the case when the object it's not
            ## orbiting any other object (probably COM).
            try: 
                obj = self.orbits[obj]
                orbit.append( obj )
            except KeyError:
                break
 
        orbit.reverse()
        return orbit


    def get_orbit_transfer(self, orig_obj: str, dest_obj: str):
        '''
        Returns the orbital transfers to get you from orbiting
        orig_obj to orbiting dest_obj.

        FixMe: the order of the objects is not reliable.
        '''
        ## *_orbit contains all the objects orbited by *_obj
        orig_orbit = self.get_orbit( orig_obj )
        dest_orbit = self.get_orbit( dest_obj )

        ## Using a set prevents from having duplicated objects.
        ##
        ## The orbit transfer path is the difference between
        ## the union and the intersection of the two orbits.
        commom_obj = set(orig_orbit).intersection(dest_orbit)
        orbit_transfer = set(orig_orbit).union(dest_orbit).difference(commom_obj)

        return list( orbit_transfer )
        

if __name__ == '__main__':
    uom = UniversalOrbitMap('input.dat')
    print('Part one: %d' % uom.checksum)
    print('Part two: %d' % len( uom.get_orbit_transfer('YOU', 'SAN') ) )

