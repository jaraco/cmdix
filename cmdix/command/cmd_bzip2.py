from __future__ import print_function, unicode_literals
from ..compressor import compressor


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    return compressor(p, 'bzip2')
