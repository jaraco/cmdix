import os
import re
import subprocess

from more_itertools import partition


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
    p.add_argument("inputs", nargs="*")
    return p


def func(args):
    handler = invoke if args.inputs else print_env
    return handler(args)


def print_env(args):
    for k, v in args.env.items():
        print(k + '=' + v)


class VarsCheck:
    """
    Partition inputs to env into vars and cmd args.

    >>> vars, cmd = VarsCheck().partition(['foo=bar', 'bing=baz', 'blue', 'z=3'])
    >>> dict(vars)
    {'foo': 'bar', 'bing': 'baz'}
    >>> list(cmd)
    ['blue', 'z=3']
    """

    nonvar = False

    def __call__(self, input):
        return self.nonvar or self._check(input)

    def _check(self, input):
        self.nonvar = not re.match(r'\w+=.*$', input)
        return self.nonvar

    def partition(self, inputs):
        vars, cmd = partition(self, inputs)
        return map(_split, vars), cmd


def _split(var):
    return var.split('=', maxsplit=1)


def invoke(args):
    vars, cmd = VarsCheck().partition(args.inputs)
    args.env.update(vars)
    return subprocess.Popen(cmd, env=args.env).wait()
