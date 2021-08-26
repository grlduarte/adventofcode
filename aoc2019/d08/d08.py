'''
gduarte@astro.ufsc.br
Created on 20-Apr-2020
'''

class SpaceImageFormatDecoder:
    def __init__(self, image_file: str, width: int, height: int):
        '''
        Decodes images in the Space Image Format (SIF).
        '''
        self.filename = image_file
        self.width    = width
        self.height   = height
        with open(self.filename) as f:
            self.encoded = f.read().strip()
       
        ## Calculates the countcheck and then decodes the image
        self._split_to_layers()
        self._calc_countcheck()
        self._decode()


    def __str__(self):
        '''
        When calling print(object) this method is used.

        Replaces the white pixels (value 1) by unicode blocks
        \u25A0 and the black pixels (value 0) by spaces.
        '''
        return self.decoded.replace('0',' ').replace('1','\u25A0')


    def _split_to_layers(self):
        '''
        Splits the encoded image to its layers.
        '''
        layer_size = self.width * self.height
        layers = []

        ## Append to layers each section of layer_size characters
        for px in range(0, len(self.encoded), layer_size):
            layers.append( self.encoded[px : px + layer_size] )
        self._layers = layers


    def _calc_countcheck(self):
        zeros_count = [ layer.count('0') for layer in self._layers ]
        min_count_layer = self._layers[ zeros_count.index( min(zeros_count) ) ]
        self.countcheck = min_count_layer.count('1') * min_count_layer.count('2')


    def _decode(self):
        ## Strings are immutable so you must convert it
        ## to a list
        stacked_layer = list( self._layers[-1] )

        ## The last layer is the base one. If the pixels
        ## in the upper layers are not transparent (pixel
        ## value 1 or 2) replace them in the layer below.
        ## Do that until it reaches the top layer.
        for layer in reversed(self._layers):
            for px,value in enumerate( list(layer) ):
                if (value == '0') or (value == '1'):
                    stacked_layer[px] = value

        ## Get it back to the string form
        stacked_layer = "".join(stacked_layer)

        ## Split into rows. Logic is pretty similiar
        ## to the layer splitting.
        rows = ''
        for px in range(0, len(stacked_layer), self.width):
            rows += stacked_layer[px : px + self.width] + '\n'
        self.decoded = rows


if __name__ == '__main__':
    image = SpaceImageFormatDecoder('input.dat', 25, 6)
    print("Part one: %d" % image.countcheck )
    print(image)
    print("Part two: %s" % image.decoded.replace('\n','') )

