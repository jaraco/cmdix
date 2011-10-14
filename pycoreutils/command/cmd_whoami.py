#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os

try:
    import pwd
except ImportError as err:
    pass


@pycoreutils.addcommand
@pycoreutils.onlyunix
def whoami(p):
    p.set_defaults(func=func)
    p.description = "Print the user name associated with the current" + \
                    "effective user ID.\nSame as id -un."


def func(args):
    print(pwd.getpwuid(os.getuid())[0])
