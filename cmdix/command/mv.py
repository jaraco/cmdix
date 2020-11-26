import shutil


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Move SOURCE to DEST"
    p.add_argument("SOURCE", nargs='+')
    p.add_argument("DEST", nargs=1)
    p.add_argument(
        "-v", "--verbose", action="store_true", help="explain what is being done"
    )
    return p


def func(args):
    for args.SOURCE in args:
        if args.verbose:
            print("'{0}' -> '{1}'".format(args.SOURCE, args.DESTINATION))

        shutil.move(args.SOURCE, args.DESTINATION)
