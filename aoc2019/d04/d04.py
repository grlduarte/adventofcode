
def check_increasing(digits: str):
    '''
    Return True if the input string is in increasing order.

    The  built-in function sorted sorts a string into a list
    following  ascending order  (both numerical and alphabet-
    ical). If the input string is equal its sorted form,  it
    is increasing.
    '''
    return( digits == "".join( sorted(digits) ) )


def check_repeated(digits: str):
    '''
    Return  True if  there are  repeated  adjacent digits in
    the input string.

    The  built-in  function any  returns  True if any of the
    input values is True.  In this  case,  it checks whether
    there is some digit  count greater  than 1 in the input.
    Note  this only  works  because  we already  checked the
    digits are increasing earlier.

    '''
    return any( c > 1 for c in [ digits.count(_) for _ in digits ] )


def check_double(digits):
    '''
    Return True if any  of the repeated digits are only dou-
    bles.

    Checks whether there is or there is not some digit with
    exactly two counts in the input string. Note this alone
    is not enough to satisfy the criteria.
    '''
    return( 2 in [ digits.count(_) for _ in digits ] )


def make_increasing(digits: str):
    '''
    Return the next password with only increasing digits.
    '''
    ldigits = list(digits)
    for i in range(1, len(ldigits) ):
        if ldigits[i] < ldigits[i-1]:
            ldigits[i] = ldigits[i-1]
    return( "".join( ldigits ) )


if __name__ == '__main__':
    with open('input.dat', 'r') as f:
        pw_i, pw_f = f.read().strip().split()
    
    pw = int(pw_i)
    
    # These counts the number of valid passwords found for each part
    # I'm not checking if len(pw) == 6 but maybe I should.
    valid_pw_one = 0 
    valid_pw_two = 0 
    while pw < int(pw_f):
        digits = str(pw)
        if check_increasing(digits):
            pw += 1
            if check_repeated(digits):
                valid_pw_one += 1
                if check_double(digits):
                    valid_pw_two += 1
        else:
            # If the digits are not increasing, jumps to the next 
            # password with only increasing digits. This makes the
            # program run about 100 times faster
            digits = make_increasing(digits)
            pw = int("".join(digits) )

    print("Part one: %d" % valid_pw_one )
    print("Part two: %d" % valid_pw_two )
