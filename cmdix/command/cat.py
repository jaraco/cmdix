import sys
import itertools

from .. import lib


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Concatenate FILE(s), or standard input, " + "to standard output."
    p.epilog = (
        "If the FILE ends with '.bz2' or '.gz', the file will be "
        + "decompressed automatically."
    )
    p.add_argument('FILE', nargs='*')
    return p


def func(args):
    lines = itertools.chain.from_iterable(lib.parsefilelist(args.FILE, True))
    for line in lines:
        sys.stdout.write(line)
