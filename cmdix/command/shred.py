import logging
import os
import random


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Overwrite the specified FILE(s) repeatedly, in order "
        + "to make it harder for even very expensive hardware "
        + "probing to recover the data."
    )
    p.epilog = (
        "This program acts as GNU 'shred -x', and doesn't round "
        + "sizes up to the next full block"
    )
    p.add_argument('FILE', nargs='*')
    p.add_argument(
        "-n",
        "--iterations",
        dest="iterations",
        default=3,
        help="overwrite ITERATIONS times instead of the default (3)",
    )
    p.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose", help="show progress"
    )
    return p


def func(args):
    for arg in args.FILE:
        for i in range(args.iterations):
            size = os.stat(arg).st_size
            fd = open(arg, mode='w')
            logging.debug('Size:', size)
            fd.seek(0)
            for i in range(size):
                # Get random byte
                b = "".join(chr(random.randrange(0, 256)))
                fd.write(b)
            fd.close()
