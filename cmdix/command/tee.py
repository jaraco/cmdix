import sys

from .. import onlyunix


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Copy standard input to each FILE, and also to " + "standard output."
    )
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-a",
        "--append",
        action="store_true",
        dest="append",
        help="append to the given FILEs, do not overwrite",
    )
    return p


def func(args):
    fdlist = []
    for filename in args.FILE:
        if args.append:
            fdlist.append(open(filename, 'a'))
        else:
            fdlist.append(open(filename, 'w'))

    for line in sys.stdin.readlines():
        sys.stdout.write(line)
        for fd in fdlist:
            fd.write(line)
