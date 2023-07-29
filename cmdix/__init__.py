import sys

import argparse
import os
import shlex
import platform
from importlib import metadata

import importlib_resources as resources

from . import command
from .exception import CommandNotFoundException


__version__ = metadata.version(__name__)


def onlyunix(f):
    """
    Decorator that indicates that the command cannot be run on windows
    """
    f._onlyunix = True
    return f


def format_all_help():
    """
    Yields (commandname, commandhelp) for all available commands.
    """
    for commandname in listcommands():
        cmd = getcommand(commandname)
        p = cmd(argparse.ArgumentParser(prog=commandname))
        yield (commandname, p.format_help())


def _is_available(name):
    try:
        cmd = _get_command(name)
        needs_unix = getattr(cmd, '_onlyunix', False)
        is_windows = platform.system() == 'Windows'
        return not (needs_unix and is_windows)
    except CommandNotFoundException:
        return False


def _get_command(name):
    # Try to import the command module
    importstring = f'cmdix.command.{name}'
    try:
        return __import__(importstring, fromlist=1).parseargs
    except ImportError:
        raise CommandNotFoundException(name)


def getcommand(commandname):
    """
    Returns the `parseargs`-function of the given commandname.
    Raises a CommandNotFoundException if the command is not found
    """
    cmd = _get_command(commandname)
    if not _is_available(commandname):
        raise CommandNotFoundException(commandname)
    return cmd


def listcommands():
    """
    Returns a list of all available commands
    """
    paths = resources.files(command).iterdir()
    all = (path.stem for path in paths if not path.name.startswith('_'))
    return filter(_is_available, all)


def _gen_script_definitions():
    print('console_scripts =')
    for cmd in listcommands():
        print(f'\t{cmd} = cmdix:run')


def get_parser(commandname):
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Coreutils in Pure Python.",
        prog=commandname,
        epilog="Available Commands: " + ", ".join(listcommands()),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("command", nargs="?")
    group.add_argument(
        "--allhelp", action="store_true", help="Show the help pages off all commands"
    )
    group.add_argument(
        "--license", action="store_true", help="Show program's license and exit"
    )
    group.add_argument("--runtests", action="store_true", help="Run all sort of tests")
    return parser


def run(argv=None):
    """
    Parse commandline arguments and run command.
    If argv is None, read from sys.argv.

    For example:

    >>> import cmdix
    >>> cmdix.run(['seq', '-s', ' to the ', '1', '4'])
    1 to the 2 to the 3 to the 4

    :param argv:    List of arguments
    :return:        The exit status of the command. None means 0.
    """
    argv = argv or sys.argv
    commandname = os.path.basename(argv[0])
    argv = argv[1:]
    parser = get_parser(commandname)

    if commandname in ('__main__.py',):
        args, argv = parser.parse_known_args(argv)

        if handle_args(parser, args, argv):
            return

        commandname = args.command

    return run_subcommand(commandname, argv)


def handle_args(parser, args, argv):
    if args.license:
        print("MIT")
        return True

    if args.allhelp:
        for commandname, commandhelp in format_all_help():
            print("\n" + commandname + "\n\n" + commandhelp)
        return True

    if args.runtests:
        try:
            from . import test
        except ImportError:
            print("Can't import test suite", file=sys.stderr)
            sys.exit(1)
        test.runalltests()
        return True

    if not args.command and not argv:
        parser.print_help()
        return True


def run_subcommand(commandname, argv):
    """
    Run the subcommand
    """
    try:
        cmd = getcommand(commandname)
    except CommandNotFoundException:
        print(f"Command `{commandname}` not found.", file=sys.stderr)
        return
    p = cmd(argparse.ArgumentParser(prog=commandname))
    args = p.parse_args(argv)
    args.func(args)


def runcommandline(commandline):
    """
    Process a commandline; main entry-point.

    Examples:

    >>> import cmdix
    >>> cmdix.runcommandline('basename /foo/bar/')
    bar
    >>> cmdix.runcommandline('cal 2 2000')
       February 2000
    Su Mo Tu We Th Fr Sa
           1  2  3  4  5
     6  7  8  9 10 11 12
    13 14 15 16 17 18 19
    20 21 22 23 24 25 26
    27 28 29

    :param commandline: String representing the commandline, i.e. "ls -l /tmp"
    """
    return run(shlex.split(str(commandline)))
