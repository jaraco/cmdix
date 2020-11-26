from .. import lib


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: GNU's sort doesn't count '/'.
    # Sorting /etc/fstab has different outcomes.
    p.set_defaults(func=func)
    p.description = "sort lines of text files"
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        dest="reverse",
        help="reverse the result of comparisons",
    )
    return p


def func(args):
    ell = []
    for line, filename in lib.parsefilelist(args.FILE):
        ell.append(line)
    ell.sort(reverse=args.reverse or False)
    print(''.join(ell), end='')
