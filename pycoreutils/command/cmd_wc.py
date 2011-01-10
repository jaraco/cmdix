#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def wc(argstr):
    # TODO: Bytes
    p = pycoreutils.parseoptions()
    p.description = "Print newline, word, and byte counts for each file"
    p.usage = "%prog [OPTION]... [FILE]..."
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " +\
               "decompressed automatically."
    p.add_option("-m", "--chars", action="store_true", dest="chars",
            help="print the character counts")
    p.add_option("-l", "--lines", action="store_true", dest="lines",
            help="print the newline counts")
    p.add_option("-w", "--words", action="store_true", dest="words",
            help="print the word counts")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    fdict = {}
    if args == []:
        args = ['-']
    for filename in args:
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
    if not opts.chars and not opts.lines and not opts.words:
        opts.chars = opts.lines = opts.words = True

    for filename, v in fdict.items():
        if opts.lines:
            yield "{0:>{l}} ".format(v['lines'], l=maxlen)
        if opts.words:
            yield "{0:>{l}} ".format(v['words'], l=maxlen)
        if opts.chars:
            yield "{0:>{l}} ".format(v['chars'], l=maxlen)
        if filename != '-':
            yield filename
        yield '\n'

    if len(fdict) > 1:
        if opts.lines:
            yield "{0:>{l}} ".format(totlines, l=maxlen)
        if opts.words:
            yield "{0:>{l}} ".format(totwords, l=maxlen)
        if opts.chars:
            yield "{0:>{l}} ".format(totchars, l=maxlen)
        yield 'total\n'
