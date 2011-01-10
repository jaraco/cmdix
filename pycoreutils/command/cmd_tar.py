#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import sys
import tarfile


@pycoreutils.addcommand
def tar(argstr):
    p = pycoreutils.parseoptions()
    p.description = "saves many files together into a single tape or disk " +\
                   "archive, and can restore individual files from the archive"
    p.usage = '%prog -x [OPTION]...\n' + \
       '       %prog -t [OPTION]...\n' + \
       '       %prog -c [OPTION]... TARFILE SOURCE...\n'
    p.epilog = "Files that end with '.bz2' or '.gz' are decompressed " +\
               "automatically."
    p.add_option("-c", "--create", action="store_true", dest="create",
            help="create zipfile from source.")
    p.add_option("-t", "--list", action="store_true", dest="list",
            help="list files in zipfile.")
    p.add_option("-x", "--extract", action="store_true", dest="extract",
            help="extract tarfile into current directory.")
    p.add_option("-j", "--bzip2", action="store_true", dest="bzip2",
            help="(de)compress using bzip2")
    p.add_option("-f", "--file", dest="archive",
            help="use archive file or device ARCHIVE")
    p.add_option("-z", "--gzip", action="store_true", dest="gzip",
            help="(de)compress using gzip")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    if bool(opts.list) + bool(opts.create) + bool(opts.extract) > 1:
        raise pycoreutils.StdErrException(
                                "You can only use one of '-c', '-t' or 'x'")

    if opts.extract or opts.list:
        if opts.archive:
            infile = open(opts.archive, 'rb')
        else:
            infile = sys.stdin
        try:
            tar = tarfile.open(fileobj=infile)
        except tarfile.TarError as err:
            raise pycoreutils.StdErrException("Could not parse file " +\
                "{0}. Are you sure it is a tar-archive?".format(infile.name))

    if opts.extract:
        tar.extractall()
        tar.close()

    elif opts.list:
        for tarinfo in tar:
            name = tarinfo.name
            if tarinfo.isdir():
                    name += '/'
            yield name + '\n'
        tar.close()

    elif opts.create:
        # Set outfile
        if opts.archive:
            outfile = open(opts.archive, 'wb')
        else:
            outfile = sys.stout

        # Set mode
        if opts.gzip:
            mode = 'w:gz'
        elif opts.bzip2:
            mode = 'w:bz2'
        else:
            mode = 'w'
        tar = tarfile.open(fileobj=outfile, mode=mode)
        for arg in args:
            tar.add(arg)
        tar.close()
    else:
        raise pycoreutils.StdErrException("Either '-c', '-t' or '-x' " +\
                                          "should be specified")
