import os
import os.path


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "print name of current/working directory"
    p.add_argument('FILE', nargs='+')
    p.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="ignore nonexistent files, never prompt",
    )
    p.add_argument(
        "-r",
        "-R",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="remove directories and their contents recursively",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="explain what is being done",
    )
    return p


def func(args):
    def _raise(err):
        if not args.force:
            raise err

    for arg in args.FILE:
        do_it(_raise, arg, args)


def do_it(_raise, arg, args):
    if args.recursive and os.path.isdir(arg):
        # Remove directory recursively
        for root, dirs, files in os.walk(arg, topdown=False, onerror=_raise):
            for name in files:
                path = os.path.join(root, name)
                os.remove(path)
                if args.verbose:
                    print("Removed file '{0}'\n".format(path))
            for name in dirs:
                path = os.path.join(root, name)
                os.rmdir(path)
                if args.verbose:
                    print("Removed directory '{0}'\n".format(path))
        os.rmdir(arg)
    else:
        # Remove single file
        try:
            os.remove(arg)
            if args.verbose:
                print("Removed '{0}'\n".format(arg))
        except OSError as err:
            _raise(err)
