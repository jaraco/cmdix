from .. import lib
import base64 as _base64
import textwrap


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Base64 encode or decode FILE, or standard input, " + "to standard output."
    )
    p.add_argument('FILE', nargs=1)
    p.add_argument("-d", action="store_true", dest="decode", help="decode data")
    p.add_argument(
        "-w",
        dest="wrap",
        default=76,
        type=int,
        help="wrap encoded lines after COLS character (default 76). "
        + "Use 0 to disable line wrapping",
    )
    return p


def func(args):
    s = ''.join(line for file in lib.parsefilelist(args.FILE) for line in file)

    if args.decode:
        out = _base64.b64decode(s.encode('ascii')).decode('ascii')
        if args.wrap == 0:
            print(out)
        else:
            for line in textwrap.wrap(out, args.wrap):
                print(line)
    else:
        out = _base64.b64encode(s.encode('ascii')).decode('ascii')
        if args.wrap == 0:
            print(out)
        else:
            for line in textwrap.wrap(out, args.wrap):
                print(line)
