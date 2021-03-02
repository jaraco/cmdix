import fileinput


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Print newline, word, and byte counts for each file"
    p.epilog = (
        "If the FILE ends with '.bz2' or '.gz', the file will be "
        + "decompressed automatically."
    )
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-m",
        "--chars",
        action="store_true",
        dest="chars",
        help="print the character counts",
    )
    p.add_argument(
        "-l",
        "--lines",
        action="store_true",
        dest="lines",
        help="print the newline counts",
    )
    p.add_argument(
        "-w", "--words", action="store_true", dest="words", help="print the word counts"
    )
    return p


def func(args):
    # TODO: Bytes
    fdict = make_fdict(args)

    totchars, totlines, totwords = count(fdict)

    maxlen = len(str(totchars))
    if not args.chars and not args.lines and not args.words:
        args.chars = args.lines = args.words = True

    report(args, fdict, maxlen, totchars, totlines, totwords)


def report(args, fdict, maxlen, totchars, totlines, totwords):
    for filename, v in fdict.items():
        if args.lines:
            print("{0:>{len}} ".format(v['lines'], len=maxlen), end='')
        if args.words:
            print("{0:>{len}} ".format(v['words'], len=maxlen), end='')
        if args.chars:
            print("{0:>{len}} ".format(v['chars'], len=maxlen), end='')
        if filename != '-':
            print(filename, end='')
        print()
    if len(fdict) > 1:
        if args.lines:
            print("{0:>{len}} ".format(totlines, len=maxlen), end='')
        if args.words:
            print("{0:>{len}} ".format(totwords, len=maxlen), end='')
        if args.chars:
            print("{0:>{len}} ".format(totchars, len=maxlen), end='')
        print('total')


def count(fdict):
    totchars = totlines = totwords = 0
    for filename, v in fdict.items():
        totchars += v['chars']
        totlines += v['lines']
        totwords += v['words']
    return totchars, totlines, totwords


def make_fdict(args):
    fdict = {}
    if args.FILE == []:
        args.FILE = ['-']
    for filename in args.FILE:
        fdict[filename] = {'chars': 0, 'lines': 0, 'words': 0}
        for line in fileinput.input(filename, openhook=fileinput.hook_compressed):
            fdict[filename]['chars'] += len(line)
            fdict[filename]['lines'] += 1
            fdict[filename]['words'] += len(line.split())
    return fdict
