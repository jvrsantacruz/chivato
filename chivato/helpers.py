#-*- coding: utf-8 -*-

def _posint(x):
    value = int(x)
    if value < 0:
        raise ValueError('not a positive integer')
    return value


def mult_add(number, multiplier=2):
    '''Sum each digits of the multiplication of i and j. '''
    return sum(int(n) for n in str(number * multiplier))


def mod1110(value):
    '''
    Compute ISO 7064, Mod 11,10
    '''
    t = 10
    for i in value:
        c = int(i)
        t = (2 * ((t + c) % 10 or 10)) % 11
    return (11 - t) % 10
