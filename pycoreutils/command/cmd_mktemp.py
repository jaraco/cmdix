# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import sys
import tempfile


@pycoreutils.addcommand
def mktemp(p):
    # TODO: Templates, most of the options
    p.set_defaults(func=func)
    p.description = "Create a temporary file or directory, safely, and " + \
                    "print its name."
    p.usage = '%(prog)s [OPTION]... [TEMPLATE]'
    p.add_argument("-d", "--directory", action="store_true", dest="directory",
            help="create a directory, not a file")


def func(args):
    if len(args) == 0:
        if opts.directory:
            print(tempfile.mkdtemp(prefix='tmp.'))
        else:
            print(tempfile.mkstemp(prefix='tmp.')[1])
    elif len(args) == 1:
        raise NotImplementedError("Templates are not yet implemented")
    else:
        print("mktemp: too many templates. Try `mktemp --help' for more " +\
              "information.", file=sys.stderr)
