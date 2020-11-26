import sys

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


def try_decode(line):
    try:
        return line.decode()
    except Exception:
        return line


def func(args):
    lines = (
        try_decode(line) for file in lib.parsefilelist(args.FILE, True) for line in file
    )
    for line in lines:
        sys.stdout.write(line)
