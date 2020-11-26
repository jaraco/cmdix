import os


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "print name of current/working directory"
    p.add_argument(
        "-L",
        "--logical",
        action="store_true",
        dest="logical",
        help="use PWD from environment, even if it contains symlinks",
    )
    p.add_argument(
        "-P",
        "--physical",
        action="store_true",
        dest="physical",
        help="avoid all symlinks",
    )
    return p


def func(args):
    if args.logical:
        print(os.getenv('PWD'))
    elif args.physical:
        print(os.path.realpath(os.getcwd()))
    else:
        print(os.getcwd())
