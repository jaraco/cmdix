from ..exception import StdErrException
import sys
import tarfile


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "saves many files together into a single tape or disk "
        "archive, and can restore individual files from the archive"
    )
    p.usage = (
        '%(prog)s -x [OPTION]...\n'
        '       %(prog)s -t [OPTION]...\n'
        '       %(prog)s -c [OPTION]... TARFILE SOURCE...\n'
    )
    p.epilog = (
        "Files that end with '.bz2' or '.gz' are decompressed " + "automatically."
    )
    p.add_argument('FILE', nargs="*")
    p.add_argument(
        "-c",
        "--create",
        action="store_true",
        dest="create",
        help="create zipfile from source.",
    )
    p.add_argument(
        "-t", "--list", action="store_true", dest="list", help="list files in zipfile."
    )
    p.add_argument(
        "-x",
        "--extract",
        action="store_true",
        dest="extract",
        help="extract tarfile into current directory.",
    )
    p.add_argument(
        "-j",
        "--bzip2",
        action="store_true",
        dest="bzip2",
        help="(de)compress using bzip2",
    )
    p.add_argument(
        "-f", "--file", dest="archive", help="use archive file or device ARCHIVE"
    )
    p.add_argument(
        "-z", "--gzip", action="store_true", dest="gzip", help="(de)compress using gzip"
    )
    return p


def func(args):
    if bool(args.list) + bool(args.create) + bool(args.extract) > 1:
        print("You may not specify more than one of '-ctx'", file=sys.stderr)
        sys.exit(2)

    if args.extract or args.list:
        if args.archive:
            infile = open(args.archive, 'rb')
        else:
            infile = sys.stdin
        try:
            tar = tarfile.open(fileobj=infile)
        except tarfile.TarError:
            raise StdErrException(
                "Could not parse file {0}. Are you sure it is a tar-archive?".format(
                    infile.name
                )
            )

    if args.extract:
        tar.extractall()
        tar.close()

    elif args.list:
        list_(tar)

    elif args.create:
        create(args)
    else:
        print("Either '-c', '-t' or '-x' should be specified", file=sys.stderr)


def list_(tar):
    for tarinfo in tar:
        name = tarinfo.name
        if tarinfo.isdir():
            name += '/'
        print(name)
    tar.close()


def create(args):
    # Set outfile
    if args.archive:
        outfile = open(args.archive, 'wb')
    else:
        outfile = sys.stout
    # Set mode
    if args.gzip:
        mode = 'w:gz'
    elif args.bzip2:
        mode = 'w:bz2'
    else:
        mode = 'w'
    tar = tarfile.open(fileobj=outfile, mode=mode)
    for arg in args.FILE:
        tar.add(arg)
    tar.close()
    if args.archive:
        outfile.close()
