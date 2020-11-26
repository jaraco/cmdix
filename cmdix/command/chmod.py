import os
import subprocess


from .. import onlyunix


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Testing!!!
    p.set_defaults(func=func)
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = "%(prog)s NEWROOT [COMMAND [ARG]...]\nor:    %(prog)s [OPTION]"
    return p


def func(args):
    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    os.chroot(args[0])
    subprocess.call(args)
