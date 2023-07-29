from .. import lib
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Everything!!!!!!!!
    p.set_defaults(func=func)
    p.description = (
        "Print the last 10 lines of each FILE to standard "
        + "output. With more than one FILE, precede each with a "
        + "header giving the file name. With no FILE, or when "
        + "FILE is -, read standard input."
    )
    p.add_argument('FILE', nargs="*")
    p.add_argument(
        "-f",
        "--follow",
        action="store_true",
        help="output appended data as the file grows",
    )
    p.add_argument(
        "-i",
        "--interval",
        default=1,
        type=float,
        help="When using 'follow', check the file every INTERVAL seconds",
    )
    p.add_argument(
        "-n",
        "--lines",
        default=10,
        metavar="N",
        help="output the last N lines, instead of the last 10",
        type=int,
    )
    return p


def func(args):
    fds = lib.filelist2fds(args.FILE)
    if args.follow:
        while True:
            time.sleep(args.interval)
            for fd in fds:
                where = fd.tell()
                line = fd.readline()
                if not line:
                    fd.seek(where)
                else:
                    print(line, end='')
    else:
        for fd in fds:
            pos, lines = args.lines + 1, []
            while len(lines) <= args.lines:
                try:
                    fd.seek(-pos, 2)
                except OSError:
                    fd.seek(0)
                    break
                finally:
                    lines = list(fd)
                pos *= 2
            for line in lines[-args.lines :]:
                print(line, end='')

    """
    if args.follow:
        # tail -f
        print('G'*99, args.interval)
        while 1:
            for fd in fdlist:
                fd.seek(0, 2)
                lines = fd.readlines()
                if lines:
                    for line in lines:
                        print(line)
                        yield line
                    time.sleep(1)
    """
