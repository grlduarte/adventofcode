'''
gduarte@astro.ufsc.br
Created on 21-Apr-2020
'''

class Computer:
    def __init__(self, input_file: str, mem_alloc=2048, video=None):
        with open(input_file, 'r') as f: 
            self.intcode = [int(_) for _ in f.read().strip().split(',')]
        
        self.mem_alloc = mem_alloc
        self.video = video
        self.reset()
        self._operations = { 1: self._sum,          2: self._multiply,
                             3: self._get_input,    4: self._set_output,
                             5: self._jump_if_true, 6: self._jump_if_false,
                             7: self._less_than,    8: self._equal_to,
                             9: self._set_rel_base, 99: self._halt }

    def reset(self):
        '''
        Loads the  reset program  to the memory and set the
        pointer to 0.
        '''
        self.memory = self.intcode[:]
        self.memory.extend( (0 for _ in range(self.mem_alloc - len(self.intcode))) )
        self.status = 'stopped'
        self.pointer = 0
        self.output = []
        self.screen = [[0 for _ in range(self.video.y_size)] for _ in range(self.video.x_size)]
        self.score = 0
        self.rel_base = 0
        self.verbose = False

    def cycle(self, signal_input: int = None, verbose=False):
        '''
        Runs the computer from the current pointer. If some
        input is required the computer is set to the status
        waiting_input.

        Verbose mode prints every output to stdout,  useful
        for diagnostic tests.
        '''
        self._input = signal_input
        self.status = 'running'
        self.verbose = verbose
        self.read_instruction()
        self.video.update()

    def _read_modes(self):
        '''
        This method handles the instruction and sets the op-
        code and modes.
        '''
        ## Fill the instruction with zeros to the left
        instruction = f"{self.memory[self.pointer]:05}"

        self._opcode = int( instruction[3:] )
        modes = [int(mode) for mode in instruction[:3]]
        modes.reverse()

        self._addresses = []
        for i,m in enumerate(modes):
            try:
                ## If the pointer is at the end of the program, it would
                ## try to read positions out of the memory. If that's not the
                ## case the opcode may be corrupted. When any of that happens,
                ## append None to the addresses.
                if m == 0:
                    self._addresses.append( self.memory[self.pointer + i + 1] )
                elif m == 1:
                    self._addresses.append( self.pointer + i + 1 )
                elif m == 2:
                    self._addresses.append( self.memory[self.pointer + i + 1] + self.rel_base)
                else:
                    self._halt(with_error=True)
            except IndexError:
                self._addresses.append(None)

    ### These methods are the functions for each opcode ###
    def _sum(self):
        add1, add2, add3 = self._addresses
        self.memory[add3] = self.memory[add1] + self.memory[add2]
        self.pointer += 4

    def _multiply(self):
        add1, add2, add3 = self._addresses
        self.memory[add3] = self.memory[add1] * self.memory[add2]
        self.pointer += 4

    def _get_input(self):
        add1, *_ = self._addresses
        assert type(self._input) is int
        self.memory[add1] = self._input
        self.pointer += 2
        self._input = None

    def _set_output(self):
        add1, *_ = self._addresses
        self.output.append(self.memory[add1])
        if self.verbose: print(self.output[-1], end=' ')
        if len(self.output) == 3:
            self.handle_output()
        self.pointer += 2

    def _jump_if_true(self):
        add1, add2, _ = self._addresses
        if self.memory[add1] != 0:
            self.pointer = self.memory[add2]
        else: self.pointer += 3

    def _jump_if_false(self):
        add1, add2, _ = self._addresses
        if self.memory[add1] == 0:
            self.pointer = self.memory[add2]
        else: self.pointer += 3

    def _less_than(self):
        add1, add2, add3 = self._addresses
        if self.memory[add1] < self.memory[add2]:
            self.memory[add3] = 1
        else:
            self.memory[add3] = 0
        self.pointer += 4

    def _equal_to(self):
        add1, add2, add3 = self._addresses
        if self.memory[add1] == self.memory[add2]:
            self.memory[add3] = 1
        else:
            self.memory[add3] = 0
        self.pointer += 4

    def _set_rel_base(self):
        add1, *_ = self._addresses
        self.rel_base += self.memory[add1]
        self.pointer += 2

    def _halt(self, with_error=False):
        self.status = "halt"
        if with_error:
            raise RuntimeError("Memory overflow")
    #######################################################
        
    def handle_output(self):
        x, y, value = self.output
        if (x == -1) and (y == 0):
            self.score = value
            print(self.score)
        else:
            self.screen[y][x] = value
        self.output = []

    def read_instruction(self):
        '''
        Read and executes  the instruction  at the  current
        pointer.
        '''
        ## Get the opcode and modes from the instruction
        try:
            self._read_modes()
            self._operations[self._opcode]()
        except (KeyError, IndexError, TypeError):
            ## If the opcode is anything that isn't in the operations
            ## dictionary it'll raise a KeyError. Also, if any of the
            ## operations tries to set some position out of the memory,
            ## it'll raise an IndexError or a TypeError if the address
            ## set as None by self._read_modes is used.
            self._halt(with_error=True)
        except AssertionError:
            ## Handling self._get_input AssertionError
            ## Assert will raise an AssertionError if the condition is not met.
            ## In that case, the program stops until it gets an input. If the
            ## input is there, save it to the memory and then clean the input.
            if self.verbose: print("Waiting input...")
            self.status = 'waiting_input'
