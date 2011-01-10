#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import random
import sys


@pycoreutils.addcommand
def shuf(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Write a random permutation of the input lines to " + \
                    "standard output."
    p.usage = '%prog [OPTION]... [FILE]\nor:    %prog -e [OPTION]... ' + \
              '[ARG]...\nor:    %prog -i LO-HI [OPTION]...'
    p.add_option("-e", "--echo", action="store_true", dest="echo",
            help="treat each ARG as an input line")
    p.add_option("-i", "--input-range", dest="inputrange",
            help="treat each number LO through HI as an input line")
    p.add_option("-n", "--head-count", dest="headcount",
            help="output at most HEADCOUNT lines")
    p.add_option("-o", "--output", dest="output",
            help="write result to OUTPUT instead of standard output")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    lines = ''
    outfd = sys.stdout

    # Write to file if -o is specified
    if opts.output:
        outfd = open(opts.output, 'w')

    if opts.echo:
        if opts.inputrange:
            pycoreutils.StdErrException(
                        "{0}: cannot combine -e and -i options".format(prog))

        lines = args
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line + '\n')

    elif len(args) > 1:
        raise pycoreutils.ExtraOperandException(prog, args[1])

    elif opts.inputrange:
        (lo, hi) = opts.inputrange.split('-')
        lines = list(range(int(lo), int(hi) + 1))
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line + '\n')

    else:
        # Use stdin for input if no file is specified
        if len(args) == 0:
            fd = sys.stdin
        else:
            fd = open(args[0])

        lines = fd.readlines()
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line)
