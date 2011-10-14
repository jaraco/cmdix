# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os


@pycoreutils.addcommand
def env(p):
    # TODO: --unset
    p.set_defaults(func=func)
    p.description = "Set each NAME to VALUE in the environment and run " + \
                    "COMMAND."
    p.usage = '%(prog)s [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_argument('command')
    p.add_argument("-i", "--ignore-environment", action="store_true",
            dest="ignoreenvironment", help="start with an empty environment")


def func(args):
    env = {}
    if not args.ignoreenvironment:
        env = os.environ

    if len(args) == 0:
        for k, v in env.items():
            print(k + '=' + v)
    else:
        for arg in args:
            x = arg.split('=')
            if len(x) < 2:
                pycoreutils.StdErrException(
                        "Invalid argument {0}. ".format(arg) +\
                        "Arguments should be in the form of 'foo=bar'", 127)
            else:
                print(x[0] + '=' + x[1])
