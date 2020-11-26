import tempfile


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Templates, most of the options
    p.set_defaults(func=func)
    p.description = (
        "Create a temporary file or directory, safely, and " + "print its name."
    )
    p.add_argument(
        "-d",
        "--directory",
        action="store_true",
        dest="directory",
        help="create a directory, not a file",
    )
    return p


def func(args):
    if args.directory:
        print(tempfile.mkdtemp(prefix='tmp.'))
    else:
        print(tempfile.mkstemp(prefix='tmp.')[1])
