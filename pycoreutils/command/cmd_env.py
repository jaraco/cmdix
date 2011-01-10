#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os


@pycoreutils.addcommand
def env(argstr):
    # TODO: --unset
    p = pycoreutils.parseoptions()
    p.description = "Set each NAME to VALUE in the environment and run " + \
                    "COMMAND."
    p.usage = '%prog [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_option("-i", "--ignore-environment", action="store_true",
            dest="ignoreenvironment", help="start with an empty environment")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    env = {}
    if not opts.ignoreenvironment:
        env = os.environ

    if len(args) == 0:
        for k, v in env.items():
            yield k + '=' + v + "\n"
    else:
        for arg in args:
            x = arg.split('=')
            if len(x) < 2:
                pycoreutils.StdErrException(
                        "Invalid argument {0}. ".format(arg) +\
                        "Arguments should be in the form of 'foo=bar'", 127)
            else:
                yield x[0] + '=' + x[1] + "\n"
