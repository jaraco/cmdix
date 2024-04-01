import abc
import argparse
import itertools
import os
import re
import subprocess

from more_itertools import partition, replace


def parseargs(p):
    p.__class__ = CustomParser
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


class Latching(metaclass=abc.ABCMeta):
    """
    A callable that once it returns something True, always returns that value.
    """

    def __call__(self, input):
        try:
            return self.__saved
        except AttributeError:
            if result := self._check(input):
                self.__saved = result
            return result

    @abc.abstractmethod
    def _check(self, input): ...  # pragma: no cover


class VarsCheck(Latching):
    """
    Partition inputs to env into vars and cmd args.

    >>> vars, cmd = VarsCheck().partition(['foo=bar', 'bing=baz', 'blue', 'z=3'])
    >>> dict(vars)
    {'foo': 'bar', 'bing': 'baz'}
    >>> list(cmd)
    ['blue', 'z=3']
    """

    def _check(self, input):
        return not re.match(r'\w+=.*$', input)

    def partition(self, inputs):
        vars, cmd = partition(self, inputs)
        return map(_split, vars), cmd


class OptsCheck(Latching):
    def _check(self, input):
        return not input.startswith('-')


class CustomParser(argparse.ArgumentParser):
    """
    Override default argument parsing to provide env-specific behaviors.
    """

    def parse_args(self, args):
        return super().parse_args(self._replace_args(args))

    @staticmethod
    def _replace_args(args):
        """
        Separate env options from the rest of the command.

        Argparse expects `--` to separate options from position args,
        so inject that after any env options.

        Also, replace `-` with `-i` (in env options).

        >>> CustomParser._replace_args(['--help', '-', 'ENV=val', 'cmd', '-m'])
        ['--help', '-i', '--', 'ENV=val', 'cmd', '-m']
        """
        env_opts, rest = partition(OptsCheck(), args)
        repl_opts = replace(env_opts, '-'.__eq__, ('-i',))
        return list(itertools.chain(repl_opts, ('--',), rest))


def _split(var):
    return var.split('=', maxsplit=1)


def invoke(args):
    vars, cmd = VarsCheck().partition(args.inputs)
    args.env.update(vars)
    return subprocess.Popen(cmd, env=args.env).wait()
