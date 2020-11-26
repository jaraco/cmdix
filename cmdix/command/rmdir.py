import os


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Remove the DIRECTORY(ies), if they are empty."
    p.usage = '%(prog)s [OPTION]... DIRECTORY...'
    p.add_argument('directory', nargs='+')
    p.add_argument(
        "-p",
        "--parent",
        action="store_true",
        dest="parent",
        help="remove DIRECTORY and its ancestors; e.g., "
        + "'rmdir -p a/b/c' is similar to 'rmdir a/b/c a/b a'",
    )
    return p


def func(args):
    for arg in args.directory:
        if args.parent:
            os.removedirs(arg)
        else:
            os.rmdir(arg)
