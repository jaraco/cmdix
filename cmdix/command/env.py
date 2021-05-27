# TODO: implement command execution.

import os
from cmdix import run_subcommand

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
    p.add_argument(
        "--export",
        nargs=1,
        help="Set argument with --export NAME=VALUE"
    )
    p.add_argument(
        "--eval",
        nargs="+",
        help="Run any commands with newly updated environment, " 
            "--eval COMMAND ARGS"
    )
    return p


def func(args):
    if not args.export:
        for k, v in args.env.items():
            print(k + '=' + v)
    else:
        variable = args.export[0]
        if '=' not in variable:
            var = os.environ.get(variable)
            if var: print(var)
        else:
            key, value = variable.split("=")
            os.environ.update({key:value})
            if args.eval:
                subcommand, *new_args = args.eval
                return run_subcommand(subcommand, new_args)
