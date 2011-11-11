# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os.path


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "Change the current working directory to HOME or PATH"
    p.add_argument('PATH', nargs='?')
    return p


def func(args):
    if not args.PATH:
        pth = pycoreutils.getuserhome()
    else:
        pth = os.path.expanduser(args.PATH)
    os.chdir(pth)
