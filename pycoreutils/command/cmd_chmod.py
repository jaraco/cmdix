#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import subprocess


@pycoreutils.addcommand
@pycoreutils.onlyunix
def chroot(argstr):
    # TODO: Testing!!!
    p = pycoreutils.parseoptions()
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = "%prog NEWROOT [COMMAND [ARG]...]\nor:    %prog [OPTION]"
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    os.chroot(args[0])
    subprocess.call(args)
