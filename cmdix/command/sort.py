"""
>>> from unittest import mock
>>> args = mock.Mock()
>>> args.FILE = [__file__]
>>> args.reverse = False
>>> func(args)
<BLANKLINE>
...
>>> args.reverse = True
>>> func(args)
import itertools
...
"""

import itertools

from .. import lib


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: GNU's sort doesn't count '/'.
    # Sorting /etc/fstab has different outcomes.
    p.set_defaults(func=func)
    p.description = "sort lines of text files"
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        dest="reverse",
        help="reverse the result of comparisons",
        default=False,
    )
    return p


def func(args):
    lines = itertools.chain.from_iterable(lib.parsefilelist(args.FILE))
    rendered = sorted(lines, reverse=args.reverse)
    print(''.join(rendered), end='')
