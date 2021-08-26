
class Wire():
    '''
    Cria um objeto Wire q armazena todas as posicoes
    pelas quais o fio passou.
    '''
    def __init__(self, initpos, path):
        self.pos  = [ initpos ]
        self.path = path
        self._exec_path()

    def _exec_path(self):
        '''
        Verifica q tipo de instrucao eh passada pela lista path
        e manda executar
        '''
        for p in self.path:
            if p[0] == 'U':
                self._moveUp( int(p[1:]) )
            elif p[0] == 'R':
                self._moveRight( int(p[1:]) )
            elif p[0] == 'D':
                self._moveDown( int(p[1:]) )
            else:
                self._moveLeft( int(p[1:]) )

    ## Adiciona todas as posicoes do fio a lista pos para que
    ## sejam verificadas as interseccoes depois.
    ##
    ## Poderia fazer as interseccoes de forma mais matematica!
    ## Assim vai usar muito mais memoria mas eh muito mais simples
    ##
    ## Alem disso, a parte 2 se torna mais facil com esse metodo
    def _moveUp(self, step):
        for _ in range( 0, step ):
            newpos = ( self.pos[-1][0], self.pos[-1][1]+1 )
            self.pos.append( newpos )

    def _moveRight(self, step):
        for _ in range( 0, step ):
            newpos = ( self.pos[-1][0]+1, self.pos[-1][1] )
            self.pos.append( newpos )
    
    def _moveDown(self, step):
        for _ in range( 0, step ):
            newpos = ( self.pos[-1][0], self.pos[-1][1]-1 )
            self.pos.append( newpos )

    def _moveLeft(self, step):
        for _ in range( 0, step ):
            newpos = ( self.pos[-1][0]-1, self.pos[-1][1] )
            self.pos.append( newpos )


def check_intersections(pos1, pos2):
    '''
    Checa interseccoes entre duas listas de posicoes:
        Usa o objeto built-in set q possui o metodo intersection
        e remove a interseccao no ponto de partida.
    '''
    intersections = list( set( pos1 ).intersection( pos2 ) )
    intersections.remove( (0,0) )
    return intersections


if __name__ == '__main__':
    with open('input.dat', 'r') as f:
        path1, path2 = f.readlines()
    path1 = path1.split(',')
    path2 = path2.split(',')
    
    ## Cria os dois fios partindo da mesma posicao (0,0),
    ## cada um com seu caminho
    w1 = Wire( (0,0), path1 )
    w2 = Wire( (0,0), path2 )
    
    intersections = check_intersections( w1.pos, w2.pos )

    ## Parte 1: cria uma lista com a distancia da origem ate cada uma
    ## das interseccoes e imprime a mais proxima
    dist_from_origin = [ abs(_[0]) + abs(_[1]) for _ in intersections ]
    print("Closest intersection: %s" % min(dist_from_origin) )
    
    ## Parte 2: cria uma lista com o numero de passos combinados para
    ## cada uma das interseccoes e imprime a com menor numero
    steps_from_origin = [ (w1.pos.index(_) + w2.pos.index(_)) for _ in intersections]
    print("Fewer combined steps: %d" % min(steps_from_origin) )
