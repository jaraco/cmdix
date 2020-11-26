def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Print numbers from FIRST to LAST, in steps of " + "INCREMENT."
    p.usage = (
        "%(prog)s [OPTION]... LAST\nor:    %(prog)s [OPTION]... FIRST"
        + " LAST\nor:    %(prog)s [OPTION]... FIRST INCREMENT LAST"
    )
    p.add_argument("ar", nargs='+')
    p.add_argument(
        "-s",
        "--seperator",
        dest="seperator",
        help="use SEPERATOR to separate numbers (default: \\n)",
    )
    return p


def func(args):
    if len(args.ar) == 1:
        a = list(range(1, int(args.ar[0]) + 1))
    elif len(args.ar) == 2:
        a = list(range(int(args.ar[0]), int(args.ar[1]) + 1))
    elif len(args.ar) == 3:
        a = list(range(int(args.ar[0]), int(args.ar[2]) + 1, int(args.ar[1])))
    else:
        print("seq: error: too few arguments")
        return

    if args.seperator is None:
        for x in a:
            print(str(x))
    else:
        for x in range(len(a) - 1, 0, -1):
            a.insert(x, args.seperator)
        for x in a:
            print(str(x), end='')
        print()
