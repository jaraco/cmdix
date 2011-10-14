# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import subprocess


@pycoreutils.addcommand
@pycoreutils.onlyunix
def chroot(p):
    # TODO: Testing!!!
    p.set_defaults(func=func)
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = "%(prog)s NEWROOT [COMMAND [ARG]...]\nor:    %(prog)s [OPTION]"


def func(args):
    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    os.chroot(args[0])
    subprocess.call(args)
