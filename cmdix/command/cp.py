import os
import os.path
import shutil

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."
    p.add_argument('SOURCE', nargs='+')
    p.add_argument('DIRECTORY', nargs=1)
    p.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        dest="interactive",
        help="prompt before overwrite",
    )
    p.add_argument(
        "-p",
        "--preserve",
        action="store_true",
        dest="preserve",
        help="preserve as many attributes as possible",
    )
    p.add_argument(
        "-r",
        "-R",
        "--recursive",
        action="store_const",
        default=handle_direct,
        const=handle_recursive,
        dest="handle",
        help="copy directories recursively",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="print a message for each created directory",
    )
    return p


def func(args):
    _copy = shutil.copy2 if args.preserve else shutil.copy

    (dest,) = args.DIRECTORY
    for src in args.SOURCE:
        args.handle(_copy, args, dest, src)


def handle_recursive(_copy, args, dest, src):
    # Create the base destination directory if it does not exists
    if not os.path.exists(dest):
        os.mkdir(dest)

    walk(_copy, args, dest, src)


def handle_direct(_copy, args, dest, src):
    name = os.path.basename(src)
    dstfile = os.path.join(dest, name) if os.path.isdir(dest) else dest
    _copy(src, dstfile)
    if args.verbose:
        print(f"'{src}' -> '{dstfile}'")


def walk(_copy, args, dest, src):
    # Walk the source directory
    for root, dirnames, filenames in os.walk(src):
        if root == dest:
            continue
        dstmid = root.lstrip(src)

        # Create subdirectories in destination directory
        for subdir in dirnames:
            dstdir = os.path.join(dest, dstmid, subdir)
            if not os.path.exists(dest):
                os.mkdir(dstdir)
            if args.verbose:
                print(f"'{root}' -> '{dstdir}'")

        # Copy file
        for filename in filenames:
            dstfile = os.path.join(dest, dstmid, filename)
            srcfile = os.path.join(root, filename)
            if args.interactive and os.path.exists(dstfile):
                q = input(
                    f"{args.prog}: {dstfile} already "
                    + "exists; do you wish to overwrite (y or n)?"
                )
                if q.upper() != 'Y':
                    exception.StdOutException("not overwritten", 2)
                    continue
            _copy(srcfile, dstfile)
            if args.verbose:
                print(f"'{srcfile}' -> '{dstfile}'")
