import contextlib
import shutil
import sys
from urllib.error import HTTPError
from urllib.request import build_opener

import cmdix

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Fix for Python3, recursion, proxy, progress bar, you name it...
    p.set_defaults(func=func)
    p.description = "Download of files from the Internet"
    p.add_argument("url", nargs="+", help="write documents to FILE.")
    p.add_argument(
        "-O",
        "--output-document",
        dest="outputdocument",
        help="write documents to FILE.",
    )
    p.add_argument(
        "-u",
        "--user-agent",
        dest="useragent",
        help="identify as AGENT instead of default.",
    )
    return p


def func(args):
    if args.useragent:
        useragent = args.useragent
    else:
        useragent = 'Cmdix/' + cmdix.__version__

    opener = build_opener()
    opener.addheaders = [('User-agent', useragent)]

    with (
        open(args.outputdocument, 'wb')
        if args.outputdocument
        else contextlib.nullcontext(sys.stdout.buffer)
    ) as fdout:
        for url in args.url:
            try:
                fdin = opener.open(url)
            except HTTPError as e:
                raise exception.StdErrException(f"HTTP error opening {url}: {e}")

            sys.stdout.flush()
            length = int(fdin.headers['content-length'])
            print(f"Getting {length} bytes from {url}...")

            shutil.copyfileobj(fdin, fdout)
            print("Done")
