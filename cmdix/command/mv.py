import shutil


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser

    >>> import argparse
    >>> p = parseargs(argparse.ArgumentParser())
    >>> args = p.parse_args(['foo', 'bar', 'baz'])
    >>> args.SOURCE
    ['foo', 'bar']
    >>> args.DEST
    'baz'
    """
    p.set_defaults(func=func)
    p.description = "Move SOURCE to DEST"
    p.add_argument("SOURCE", nargs='+')
    p.add_argument("DEST")
    p.add_argument(
        "-v", "--verbose", action="store_true", help="explain what is being done"
    )
    return p


def func(args):
    for src in args.SOURCE:
        if args.verbose:
            print(f"'{src}' -> '{args.DEST}'")

        shutil.move(src, args.DEST)
