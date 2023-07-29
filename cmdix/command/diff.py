# Based on the example in difflib documentation

import difflib
import os
import sys
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Compare files line by line"
    p.add_argument('FILE1')
    p.add_argument('FILE2')
    p.add_argument(
        "-l",
        "--lines",
        type=int,
        default=3,
        help='Set number of context lines (default 3)',
    )

    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "-c",
        "--context",
        action="store_true",
        help='Produce a context format diff (default)',
    )
    g.add_argument(
        "-u", "--unified", action="store_true", help='Produce a unified format diff'
    )
    g.add_argument(
        "-H", "--html", action="store_true", help="Print context-diff in html"
    )
    g.add_argument(
        "-n", "--ndiff", action="store_true", help='Produce a ndiff format diff'
    )
    return p


def func(args):
    # Get modification times
    fromdate = time.ctime(os.stat(args.FILE1).st_mtime)
    todate = time.ctime(os.stat(args.FILE2).st_mtime)

    # Open fromfile
    try:
        with open(args.FILE1) as fd:
            fromlines = fd.readlines()
    except OSError:
        print("Error opening file " + args.FILE1, file=sys.stderr)

    # Open tofile
    try:
        with open(args.FILE2) as fd:
            tolines = fd.readlines()
    except OSError:
        print("Error opening file " + args.FILE2, file=sys.stderr)

    # Create diff
    if args.unified:
        diff = difflib.unified_diff(
            fromlines, tolines, args.FILE1, args.FILE2, fromdate, todate, n=args.lines
        )
    elif args.ndiff:
        diff = difflib.ndiff(fromlines, tolines)
    elif args.html:
        diff = difflib.HtmlDiff().make_file(
            fromlines,
            tolines,
            args.FILE1,
            args.FILE2,
            context=args.context,
            numlines=args.lines,
        )
    else:
        diff = difflib.context_diff(
            fromlines, tolines, args.FILE1, args.FILE2, fromdate, todate, n=args.lines
        )

    # we're using writelines because diff is a generator
    sys.stdout.writelines(diff)
