"""
>>> from unittest import mock
>>> args = mock.Mock()
>>> args.FILE = [__file__]
>>> func(args)
"...
"""

from .. import lib
import pydoc


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "number lines of files"
    p.add_argument('FILE', nargs='*')
    return p


def func(args):
    lines = _gen_lines(args.FILE)
    pydoc.pager(''.join(lines))


def _gen_lines(files):
    for index, file in enumerate(lib.parsefilelist(files)):
        # except for first file, announce the filename
        if index != 0:
            yield "::::::::::::::\n"
            yield file._files[0] + "\n"
            yield "::::::::::::::\n"
        yield from file
