#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path
import shutil


@pycoreutils.addcommand
def cp(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."
    p.usage = "%prog [OPTION]... SOURCE... DIRECTORY"
    p.add_option("-i", "--interactive", action="store_true",
            dest="interactive", help="prompt before overwrite")
    p.add_option("-p", "--preserve", action="store_true", dest="preserve",
            help="preserve as many attributes as possible")
    p.add_option("-r", "-R", "--recursive", action="store_true",
            dest="recursive", help="copy directories recursively")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    if len(args) == 1:
        raise pycoreutils.StdErrException(
                "{0}: missing destination file operand ".format(prog) +\
                "after `{1}'. ".format(args[0]) +\
                "Try {0} --help' for more information.".format(prog))

    # Set the _copy function
    if opts.preserve:
        _copy = shutil.copy2
    else:
        _copy = shutil.copy

    dstbase = args.pop()
    for src in args:
        if opts.recursive:
            # Create the base destination directory if it does not exists
            if not os.path.exists(dstbase):
                os.mkdir(dstbase)

            # Walk the source directory
            for root, dirnames, filenames in os.walk(src):
                if root == dstbase:
                    continue
                dstmid = root.lstrip(src)

                # Create subdirectories in destination directory
                for subdir in dirnames:
                    srcdir = os.path.join(root, subdir)
                    dstdir = os.path.join(dstbase, dstmid, subdir)
                    if not os.path.exists(dstbase):
                        os.mkdir(dstdir)
                    if opts.verbose:
                        yield "`{0}' -> `{1}'\n".format(root, dstdir)

                # Copy file
                for filename in filenames:
                    dstfile = os.path.join(dstbase, dstmid, filename)
                    srcfile = os.path.join(root, filename)
                    if opts.interactive and os.path.exists(dstfile):
                        q = input("{0}: {1} already ".format(prog, dstfile) +\
                                  "exists; do you wish to overwrite (y or n)?")
                        if q.upper() != 'Y':
                            pycoreutils.StdOutException("not overwritten", 2)
                            continue
                    _copy(srcfile, dstfile)
                    if opts.verbose:
                        yield "`{0}' -> `{1}'\n".format(srcfile, dstfile)
        else:
            dstfile = dstbase
            if os.path.isdir(dstbase):
                dstfile = os.path.join(dstbase, src)
            _copy(src, dstfile)
            if opts.verbose:
                yield "`{0}' -> `{1}'\n".format(src, dstfile)
