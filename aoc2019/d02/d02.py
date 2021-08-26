
def computer(intcode, noun, verb):
    intcode[1] = noun
    intcode[2] = verb

    i = 0
    while intcode[i] != 99:
        if intcode[i] == 1:
            in1 = intcode[ intcode[i+1] ]
            in2 = intcode[ intcode[i+2] ]
            out = intcode[i+3]
            intcode[out] = in1 + in2
            i += 4

        elif intcode[i] == 2:
            in1 = intcode[ intcode[i+1] ]
            in2 = intcode[ intcode[i+2] ]
            out = intcode[i+3]
            intcode[out] = in1 * in2
            i += 4

        else:
            return "Invalid opcode!"
    return intcode[0]
    
if __name__ == "__main__":
    with open("input.dat", "r") as f:
        intcode = [ int(i) for i in f.read().split(',') ]
    
    # Part one
    print("Part one: %d" % computer(intcode[:], 12, 2) )
    
    # Part two
    output = 19690720
    ij = ( (i,j) for i in range(100) for j in range(100) )
    # Using () instead of [] creates a generator instead of a
    # list comprehension. The generator, opposite to the list,
    # doesn't takes a lot of memory usage.
    for i,j in ij:
        if computer(intcode[:],i,j) == output:
            print("Part two: 100*noun + verb = %d" % (100*i+j) )
            break
