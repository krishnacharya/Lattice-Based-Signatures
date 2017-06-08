# this list of symbols allows conversion of numbers represented until base 36
base_symbols='0123456789abcdefghijklmnopqrstuvwxyz'

def v2r(n, b): # value to representation
    """Convert a positive number n to its digit representation in base b."""
    digits = ''
    while n > 0:
        digits = base_symbols[n % b] + digits
        n  = n // b
    return digits

def r2v(digits, b): # representation to value
    """Compute the number given by digits in base b."""
    n = 0
    for d in digits:
        n = b * n + base_symbols[:b].index(d)
    return n

def b2b(digits, b1, b2):
    """Convert the digits representation of a number from base b1 to base b2."""
    return v2r(r2v(digits, b1), b2)