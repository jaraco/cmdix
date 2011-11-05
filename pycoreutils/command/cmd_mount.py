# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import ctypes
import sys


@pycoreutils.addcommand
@pycoreutils.onlyunix
def mount(p):
    available_filesystems = get_available_filesystems()
    available_filesystems.sort()

    p.set_defaults(func=func)
    p.description = "Mount a filesystem"
    p.add_argument('SOURCE', nargs='?')
    p.add_argument('DEST', nargs='?')
    p.add_argument("-a", "--all", action="store_true",
            help="ignore, for compatibility with other versions")
    #p.add_argument("-o", "--options", default=0,
            #help="print only the effective group ID")
    p.add_argument("-t", "--types", default="ext2",
            help="Filesystem type. Supported types: " +\
                 ", ".join(available_filesystems))


def func(args):
    if args.SOURCE and args.DEST:
        _mount(args.SOURCE, args.DEST, args.types)
    elif args.SOURCE:
        try:
            with open('/etc/fstab') as fd:
                lines = fd.readlines()
        except IOError:
            print("Error: Couldn't read /etc/ftab", file=sys.strerr)
            return
        for line in lines:
            source, dest, fstype, options, freq, passno = line.split()
            if source == args.SOURCE:
                return _mount(source, dest, fstype)
            elif dest == args.SOURCE:
                return _mount(source, dest, fstype)
        print(args.SOURCE + " not found in /etc/fstab", file=sys.stderr)
    else:
        try:
            print(open('/etc/mtab').read().strip())
        except IOError:
            print("Error: Couldn't read /etc/mtab", file=sys.strerr)


def _mount(source, dest, fstype, options=0, data=''):
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    res = libc.mount(str(source), str(dest), str(fstype), options, str(data))
    if res < 0:
        print("Error: Mounting {0} on {1} failed!".format(source, dest),
              file=sys.strerr)


def get_available_filesystems():
    l = []
    try:
        with open('/proc/filesystems') as fd:
            for line in fd.readlines():
                l.append(line.split()[-1])
    except IOError:
        print("Error reading supported filesystems from /proc/filesystems",
              file=sys.strerr)
        return
    return l
