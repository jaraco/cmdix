# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import platform


@pycoreutils.addcommand
def arch(p):
    p.set_defaults(func=func)
    p.description = "Print machine architecture."


def func(args):
    print(platform.machine())
