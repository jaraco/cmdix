from __future__ import print_function, unicode_literals
from ..hasher import hasher


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    return hasher('sha384', p)
