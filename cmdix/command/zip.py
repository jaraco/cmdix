import os
import sys
import zipfile

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "package and compress (archive) files"
    p.usage = (
        '%(prog)s -l [OPTION]... ZIPFILE...\n'
        '       %(prog)s -t [OPTION]... ZIPFILE...\n'
        '       %(prog)s -e [OPTION]... ZIPFILE TARGET\n'
        '       %(prog)s -c [OPTION]... ZIPFILE SOURCE...\n'
    )
    p.add_argument('FILE', nargs='+')
    p.add_argument('target', nargs='?')
    p.add_argument(
        "-c",
        "--create",
        action="store_true",
        dest="create",
        help="create zipfile from source.",
    )
    p.add_argument(
        "-e",
        "--extract",
        action="store_true",
        dest="extract",
        help="extract zipfile into target directory.",
    )
    p.add_argument(
        "-l", "--list", action="store_true", dest="list", help="list files in zipfile."
    )
    p.add_argument(
        "-t",
        "--test",
        action="store_true",
        dest="test",
        help="test if a zipfile is valid.",
    )
    return p


def func(args):
    if args.list:
        list_(args)

    elif args.test:
        test(args)

    elif args.extract:
        extract(args)

    elif args.create:
        create(args)

    else:
        args.parser.print_usage(sys.stderr)
        sys.exit(1)


def create(args):
    if len(args) < 2:
        args.parser.print_usage(sys.stderr)
        sys.exit(1)

    def addToZip(zf, path, zippath):
        if os.path.isfile(path):
            zf.write(path, zippath, zipfile.ZIP_DEFLATED)
        elif os.path.isdir(path):
            for nm in os.listdir(path):
                addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        else:
            exception.StdErrException(f"Can't store {path}")

    zf = zipfile.ZipFile(args[0], 'w', allowZip64=True)
    for src in args[1:]:
        addToZip(zf, src, os.path.basename(src))
    zf.close()


def extract(args):
    if len(args) != 2:
        args.parser.print_usage(sys.stderr)
        sys.exit(1)
    zf = zipfile.ZipFile(args[0], 'r')
    out = args[1]
    for path in zf.namelist():
        if path.startswith('./'):
            tgt = os.path.join(out, path[2:])
        else:
            tgt = os.path.join(out, path)

        tgtdir = os.path.dirname(tgt)
        if not os.path.exists(tgtdir):
            os.makedirs(tgtdir)
        fp = open(tgt, 'wb')
        fp.write(zf.read(path))
        fp.close()
    zf.close()


def test(args):
    if len(args) != 1:
        args.parser.print_usage(sys.stderr)
        sys.exit(1)
    zf = zipfile.ZipFile(args[0], 'r')
    badfile = zf.testzip()
    if badfile:
        sys.stderr(f"Error on file {badfile}\n")
        sys.exit(1)
    else:
        print(f"{args[0]} tested ok" + "\n")
        sys.exit(0)


def list_(args):
    if len(args) != 1:
        args.parser.print_usage(sys.stderr)
        sys.exit(1)
    zf = zipfile.ZipFile(args[0], 'r')
    zf.printdir()
    zf.close()
