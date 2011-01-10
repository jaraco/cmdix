#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os.path


@pycoreutils.addcommand
def cd(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Change the current working directory to HOME or PATH"
    p.usage = '%prog [PATH]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        pth = pycoreutils.getuserhome()
    elif len(args) == 1:
        pth = os.path.expanduser(args[0])
    else:
        raise pycoreutils.ExtraOperandException(prog, args[1])

    os.chdir(pth)
