# TODO: implement command execution.

import os


def parseargs(p):
    p.set_defaults(func=func)
    p.description = "Set each NAME to VALUE in the environment and run " + "COMMAND."
    p.usage = '%(prog)s [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_argument(
        "-i",
        "--ignore-environment",
        action="store_const",
        const=dict(),
        dest="env",
        help="start with an empty environment",
        default=os.environ,
    )
    return p


def func(args):
    for k, v in args.env.items():
        print(k + '=' + v)
