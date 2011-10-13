#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import shutil
import sys

if sys.version_info[0] == 2:
    from urllib2 import build_opener, HTTPError
else:
    from urllib.error import HTTPError
    from urllib.request import build_opener


@pycoreutils.addcommand
def wget(p):
    # TODO: Fix for Python3, recursion, proxy, progress bar, you name it...
    p.set_defaults(func=func)
    p.description = "Download of files from the Internet"
    p.add_argument("url", nargs="+",
                   help="write documents to FILE.")
    p.add_argument("-O", "--output-document", dest="outputdocument",
                   help="write documents to FILE.")
    p.add_argument("-u", "--user-agent", dest="useragent",
                   help="identify as AGENT instead of PyCoreutils/VERSION.")


def func(args):
    if args.outputdocument:
        fdout = open(args.outputdocument, 'w')
    else:
        fdout = sys.stdout

    if args.useragent:
        useragent = args.useragent
    else:
        useragent = 'PyCoreutils/' + pycoreutils.__version__

    opener = build_opener()
    opener.addheaders = [('User-agent', useragent)]

    for url in args.url:
        try:
            fdin = opener.open(url)
        except HTTPError as e:
            pycoreutils.StdErrException("HTTP error opening " +\
                                        "{0}: {1}".format(url, e))

        length = int(fdin.headers['content-length'])
        print("Getting {0} bytes from {1}...".format(length, url))

        shutil.copyfileobj(fdin, fdout)
        print("Done")
