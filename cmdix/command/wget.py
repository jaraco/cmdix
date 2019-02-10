from __future__ import print_function, unicode_literals
import shutil
import sys

import cmdix
from .. import exception

from six.moves.urllib.request import build_opener
from six.moves.urllib.error import HTTPError


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    # TODO: Fix for Python3, recursion, proxy, progress bar, you name it...
    p.set_defaults(func=func)
    p.description = "Download of files from the Internet"
    p.add_argument("url", nargs="+",
                   help="write documents to FILE.")
    p.add_argument("-O", "--output-document", dest="outputdocument",
                   help="write documents to FILE.")
    p.add_argument("-u", "--user-agent", dest="useragent",
                   help="identify as AGENT instead of default.")
    return p


def func(args):
    if args.outputdocument:
        fdout = open(args.outputdocument, 'w')
    else:
        fdout = sys.stdout

    if args.useragent:
        useragent = args.useragent
    else:
        useragent = 'Cmdix/' + cmdix.__version__

    opener = build_opener()
    opener.addheaders = [('User-agent', useragent)]

    for url in args.url:
        try:
            fdin = opener.open(url)
        except HTTPError as e:
            exception.StdErrException(
                "HTTP error opening {0}: {1}".format(url, e))

        length = int(fdin.headers['content-length'])
        print("Getting {0} bytes from {1}...".format(length, url))

        shutil.copyfileobj(fdin, fdout)
        print("Done")
