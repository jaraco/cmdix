import os.path
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Implement --date, --time and -t
    p.set_defaults(func=func)
    p.description = (
        "Update the access and modification times of each "
        + "FILE to the current time. A FILE argument that does "
        + "not exist is created empty. A FILE argument string "
        + "of - is handled specially and causes touch to"
    )
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-a", action="store_true", dest="accessonly", help="change only the access time"
    )
    p.add_argument(
        "-c",
        "--no-create",
        action="store_true",
        dest="nocreate",
        help="do not create any files",
    )
    p.add_argument(
        "-f", action="store_true", dest="thisoptionshouldbeignored", help="(ignored)"
    )
    p.add_argument(
        "-m",
        action="store_true",
        dest="modonly",
        help="change only the modification time",
    )
    p.add_argument(
        "-r",
        "--reference",
        dest="reference",
        help="use this file's times instead of current time",
    )
    return p


def func(args):
    atime = mtime = time.time()

    for arg in args.FILE:
        if not os.path.exists(arg):
            if args.nocreate:
                # Skip file
                break
            else:
                # Create empty file
                open(arg, 'w').close()

        if args.reference:
            atime = os.path.getatime(args.reference)
            mtime = os.path.getmtime(args.reference)
        if args.accessonly:
            mtime = os.path.getmtime(arg)
        if args.modonly:
            atime = os.path.getatime(arg)
        os.utime(arg, (atime, mtime))
