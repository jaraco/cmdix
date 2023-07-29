import random
import sys

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Write a random permutation of the input lines to " + "standard output."
    )
    p.usage = (
        '%(prog)s [OPTION]... [FILE]\nor:    %(prog)s -e [OPTION]... '
        + '[ARG]...\nor:    %(prog)s -i LO-HI [OPTION]...'
    )
    p.add_argument('file', nargs='?')
    p.add_argument(
        "-e",
        "--echo",
        action="store_true",
        dest="echo",
        help="treat each ARG as an input line",
    )
    p.add_argument(
        "-i",
        "--input-range",
        dest="inputrange",
        help="treat each number LO through HI as an input line",
    )
    p.add_argument(
        "-n", "--head-count", dest="headcount", help="output at most HEADCOUNT lines"
    )
    p.add_argument(
        "-o",
        "--output",
        dest="output",
        help="write result to OUTPUT instead of standard output",
    )
    return p


def func(args):
    outfd = sys.stdout

    # Write to file if -o is specified
    if args.output:
        outfd = open(args.output, 'w')

    if args.echo:
        echo(args, outfd)

    elif args.inputrange:
        input_range(args, outfd)

    else:
        other(args, outfd)


def other(args, outfd):
    # Use stdin for input if no file is specified
    if not args.file:
        fd = sys.stdin
    else:
        fd = open(args.file)
    lines = fd.readlines()
    random.shuffle(lines)
    if args.headcount:
        lines = lines[0 : int(args.headcount)]
    for line in lines:
        outfd.write(line)


def input_range(args, outfd):
    (lo, hi) = args.inputrange.split('-')
    lines = list(range(int(lo), int(hi) + 1))
    random.shuffle(lines)
    if args.headcount:
        lines = lines[0 : int(args.headcount)]
    for line in lines:
        outfd.write(line + '\n')


def echo(args, outfd):
    if args.inputrange:
        exception.StdErrException(f"{args.prog}: cannot combine -e and -i options")
    lines = args.file
    random.shuffle(lines)
    if args.headcount:
        lines = lines[0 : int(args.headcount)]
    for line in lines:
        outfd.write(line + '\n')
