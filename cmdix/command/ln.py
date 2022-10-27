import os
import sys


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Create symbolic or hard links"
    p.add_argument("source_file", nargs='+')
    p.add_argument("target", nargs='?', default='.')
    p.add_argument(
        "-s",
        "--symbolic",
        action="store_true",
        dest="symbolic",
        help="make symbolic links instead of hard links",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="print a message for each created directory",
    )
    return p


def handle_target(args):
    """
    ln allows for source_file to contain nargs='+' and target
    to indicate a target file or target dir.

    argparse can't know if an argument is a target, as
    source_file will consume all positional parameters. This
    function adjusts for that expectation.
    """
    if len(args.source_file) > 1:
        args.target = args.source_file[-1]
        args.source_file = args.source_file[:-1]


def func(args):
    handle_target(args)

    if args.symbolic:
        f = os.symlink
    else:
        f = os.link

    for src in args.source_file:
        dst = (
            os.path.join(args.target, os.path.basename(src))
            if os.path.isdir(args.target)
            else args.target
        )

        if args.verbose:
            print(f'{dst} => {src}')
        try:
            f(src, dst)
        except Exception as err:
            print(f"ln: {err}", file=sys.stderr)
