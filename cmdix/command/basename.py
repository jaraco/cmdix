import os.path


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Print NAME with any leading directory components "
        + "removed. If specified, also remove a trailing SUFFIX."
    )
    p.add_argument('name', nargs='+')
    return p


def func(args):
    b = args.name[0]

    # Remove trailing slash to make sure /foo/bar/ is the same as /foo/bar
    if len(b) > 1:
        b = b.rstrip('/')
    b = os.path.basename(b)

    if len(args.name) == 2:
        b = b.rstrip(args.name[1])

    print(b)
