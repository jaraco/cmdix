#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def wc(p):
    p.set_defaults(func=func)
    p.description = "Print newline, word, and byte counts for each file"
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " +\
               "decompressed automatically."
    p.add_argument('files', nargs='*')
    p.add_argument("-m", "--chars", action="store_true", dest="chars",
            help="print the character counts")
    p.add_argument("-l", "--lines", action="store_true", dest="lines",
            help="print the newline counts")
    p.add_argument("-w", "--words", action="store_true", dest="words",
            help="print the word counts")


def func(args):
    # TODO: Bytes
    fdict = {}
    if args.files == []:
        args.files = ['-']
    for filename in args.files:
        fdict[filename] = {'chars': 0, 'lines': 0, 'words': 0}
        for line in fileinput.input(filename,
                                    openhook=fileinput.hook_compressed):
            fdict[filename]['chars'] += len(line)
            fdict[filename]['lines'] += 1
            fdict[filename]['words'] += len(line.split())

    totchars = totlines = totwords = 0
    for filename, v in fdict.items():
        totchars += v['chars']
        totlines += v['lines']
        totwords += v['words']

    maxlen = len(str(totchars))
    if not args.chars and not args.lines and not args.words:
        args.chars = args.lines = args.words = True

    for filename, v in fdict.items():
        if args.lines:
            print("{0:>{l}} ".format(v['lines'], l=maxlen), end='')
        if args.words:
            print("{0:>{l}} ".format(v['words'], l=maxlen), end='')
        if args.chars:
            print("{0:>{l}} ".format(v['chars'], l=maxlen), end='')
        if filename != '-':
            print(filename, end='')
        print()

    if len(fdict) > 1:
        if args.lines:
            print("{0:>{l}} ".format(totlines, l=maxlen), end='')
        if args.words:
            print("{0:>{l}} ".format(totwords, l=maxlen), end='')
        if args.chars:
            print("{0:>{l}} ".format(totchars, l=maxlen), end='')
        print('total')
