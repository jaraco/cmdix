# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import curses
import sys


def parseargs(p):
    p.set_defaults(func=func)
    p.description = "Clear the terminal screen"
    return p


def func(args):
    curses.setupterm()
    sys.stdout.write(curses.tigetstr("clear"))
    sys.stdout.flush()
