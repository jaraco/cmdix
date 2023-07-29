import functools
import hashlib

from . import lib


def hasher(algorithm, p):
    """
    :param algorithm: hash algorithm
    :param p: ArgumentParser
    """

    def myhash(args):
        for fd in lib.filelist2fds(args.FILE, 'rb'):
            hasj = hashlib.new(algorithm)
            for data in iter(functools.partial(fd.read, 128), b''):
                hasj.update(data)
            print(hasj.hexdigest() + '  ' + fd.name)

    p.set_defaults(func=myhash)
    p.description = (
        f"Print or check {algorithm.upper()} "
        + "checksums. With no FILE, or when FILE is -, read "
        + "standard input."
    )
    p.add_argument('FILE', nargs='*')
    return p
