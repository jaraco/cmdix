import os

from .. import onlyunix

try:
    import pwd
except ImportError:
    pass


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Print the user name associated with the current"
        + "effective user ID.\nSame as id -un."
    )
    return p


def func(args):
    print(pwd.getpwuid(os.getuid())[0])
