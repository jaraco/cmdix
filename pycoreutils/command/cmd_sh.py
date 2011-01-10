#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
from pycoreutils.shell import PyCoreutilsShell


@pycoreutils.addcommand
def sh(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Start a shell"
    p.usage = '%prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) > 0:
        raise pycoreutils.ExtraOperandException(prog, args[0])

    return PyCoreutilsShell().cmdloop(pycoreutils.showbanner(width=80))
