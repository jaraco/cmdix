#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import sys
import zipfile


@pycoreutils.addcommand
def zip(argstr):
    '''
    Overriding a built-in command. Yes, I known :(
    '''
    p = pycoreutils.parseoptions()
    p.description = "package and compress (archive) files"
    p.usage = '%prog -l [OPTION]... ZIPFILE...\n' + \
       '       %prog -t [OPTION]... ZIPFILE...\n' + \
       '       %prog -e [OPTION]... ZIPFILE TARGET\n' + \
       '       %prog -c [OPTION]... ZIPFILE SOURCE...\n'
    p.add_option("-c", "--create", action="store_true", dest="create",
            help="create zipfile from source.")
    p.add_option("-e", "--extract", action="store_true", dest="extract",
            help="extract zipfile into target directory.")
    p.add_option("-l", "--list", action="store_true", dest="list",
            help="list files in zipfile.")
    p.add_option("-t", "--test", action="store_true", dest="test",
            help="test if a zipfile is valid.")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    if opts.list:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        zf.printdir()
        zf.close()

    elif opts.test:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        badfile = zf.testzip()
        if badfile:
            sys.stderr("Error on file {0}\n".format(badfile))
            sys.exit(1)
        else:
            return "{0} tested ok".format(args[0]) + "\n"

    elif opts.extract:
        if len(args) != 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        zf = zipfile.ZipFile(args[0], 'r')
        out = args[1]
        for path in zf.namelist():
            if path.startswith('./'):
                tgt = os.path.join(out, path[2:])
            else:
                tgt = os.path.join(out, path)

            tgtdir = os.path.dirname(tgt)
            if not os.path.exists(tgtdir):
                os.makedirs(tgtdir)
            fp = open(tgt, 'wb')
            fp.write(zf.read(path))
            fp.close()
        zf.close()

    elif opts.create:
        if len(args) < 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        def addToZip(zf, path, zippath):
            if os.path.isfile(path):
                zf.write(path, zippath, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(path):
                for nm in os.listdir(path):
                    addToZip(zf, os.path.join(path, nm),
                             os.path.join(zippath, nm))
            else:
                pycoreutils.StdErrException("Can't store {0}".format(path))

        zf = zipfile.ZipFile(args[0], 'w', allowZip64=True)
        for src in args[1:]:
            addToZip(zf, src, os.path.basename(src))

        zf.close()

    else:
        p.print_usage(sys.stderr)
        sys.exit(1)
