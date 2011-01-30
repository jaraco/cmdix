#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput
import time


@pycoreutils.addcommand
def tail(argstr):
    # TODO: Everything!!!!!!!!
    p = pycoreutils.parseoptions()
    p.description = "Print the last 10 lines of each FILE to standard " + \
                    "output. With more than one FILE, precede each with a " + \
                    "header giving the file name. With no FILE, or when " + \
                    "FILE is -, read standard input."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-f", "--follow", action="store_true", dest="follow",
            help="output appended data as the file grows")
    p.add_option("-i", "--interval", dest="interval", default=1, type="float",
            help="When using 'follow', check the file every INTERVAL seconds")
    p.add_option("-n", "--lines", dest="lines", default=10, metavar="N",
            help="output the last N lines, instead of the last 10", type="int")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        print(p.format_help())
        return

    if opts.follow:
        fds = pycoreutils.args2fds(args)
        while True:
            time.sleep(opts.interval)
            for fd in fds:
                where = fd.tell()
                line = fd.readline()
                if not line:
                    fd.seek(where)
                else:
                    print(line, end='')
    else:
        for fd in pycoreutils.args2fds(args):
            pos, lines = opts.lines + 1, []
            while len(lines) <= opts.lines:
                try:
                    fd.seek(-pos, 2)
                except IOError:
                    fd.seek(0)
                    break
                finally:
                    lines = list(fd)
                pos *= 2
            for line in lines[-opts.lines:]:
                print(line, end='')





    """
    if opts.follow:
        # tail -f
        print('G'*99, opts.interval)
        while 1:
            for fd in fdlist:
                fd.seek(0, 2)
                lines = fd.readlines()
                if lines:
                    for line in lines:
                        print(line)
                        yield line
                    time.sleep(1)
    """
