# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import stat
import time


@pycoreutils.addcommand
def ls(p):
    # TODO: Show user and group names in ls -l, correctly format dates in ls -l
    p.set_defaults(func=func)
    p.description = "List information about the FILEs (the current " + \
                    "directory by default). Sort entries " + \
                    "alphabetically if none of -cftuvSUX nor --sort."
    p.add_argument('FILE', nargs="*")
    p.add_argument("-l", "--longlist", action="store_true",
                   help="use a long listing format")


def func(args):
    filelist = args.FILE
    if not args.FILE:
        filelist = ['.']

    for arg in filelist:
        dirlist = os.listdir(arg)
        dirlist.sort()
        l = []
        sizelen = 0     # Length of the largest filesize integer
        nlinklen = 0    # Length of the largest nlink integer
        for f in dirlist:
            path = os.path.join(arg, f)
            if not args.longlist:
                print(f)
            else:
                st = os.lstat(path)
                mode = pycoreutils.mode2string(st.st_mode)
                nlink = st.st_nlink
                uid = st.st_uid
                gid = st.st_gid
                size = st.st_size
                mtime = time.localtime(st.st_mtime)
                if stat.S_ISLNK(st.st_mode):
                    f += " -> {0}".format(os.readlink(path))
                l.append((mode, nlink, uid, gid, size, mtime, f))

                # Update sizelen
                _sizelen = len(str(size))
                if _sizelen > sizelen:
                    sizelen = _sizelen

                # Update nlinklen
                _nlinklen = len(str(nlink))
                if _nlinklen > nlinklen:
                    nlinklen = _nlinklen

        for mode, nlink, uid, gid, size, mtime, f in l:
            modtime = time.strftime('%Y-%m-%d %H:%m', mtime)
            print("{0} {1:>{nlink}} {2:<5} {3:<5} {4:>{size}} {5} {6}".format(
                                mode,
                                nlink,
                                uid,
                                gid,
                                size,
                                modtime,
                                f,
                                size=sizelen,
                                nlink=nlinklen,
                                ))
