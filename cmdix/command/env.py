import os

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: --unset
    p.set_defaults(func=func)
    p.description = "Set each NAME to VALUE in the environment and run " + "COMMAND."
    p.usage = '%(prog)s [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_argument('command')
    p.add_argument(
        "-i",
        "--ignore-environment",
        action="store_true",
        dest="ignoreenvironment",
        help="start with an empty environment",
    )
    return p


def func(args):
    env = {}
    if not args.ignoreenvironment:
        env = os.environ

    if len(args) == 0:
        for k, v in env.items():
            print(k + '=' + v)
    else:
        for arg in args:
            x = arg.split('=')
            if len(x) < 2:
                exception.StdErrException(
                    "Invalid argument {0}. ".format(arg)
                    + "Arguments should be in the form of 'foo=bar'",
                    127,
                )
            else:
                print(x[0] + '=' + x[1])
