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
def whoami(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Print the user name associated with the current" + \
                    "effective user ID.\nSame as id -un."
    p.usage = '%prog [OPTION]...'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) > 0:
        raise pycoreutils.ExtraOperandException(prog, args[0])

    return pwd.getpwuid(os.getuid())[0] + "\n"
