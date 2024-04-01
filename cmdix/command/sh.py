from .. import lib
import cmd
import os
import platform
import pprint
import shlex
import subprocess
import sys

import cmdix


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Start a shell"
    p.add_argument("-c", "--command", help="Read command from string")
    p.add_argument("--nocoreutils", action="store_true", help="Do not load pycoreutils")
    return p


def func(args):
    if args.command:
        return cmdix.runcommandline(args.command)
    else:
        sh = Sh(nocoreutils=args.nocoreutils)
        return sh.cmdloop(lib.showbanner(width=80))


class Sh(cmd.Cmd):
    """
    Shell
    """

    exitstatus = 0
    prompttemplate = '{username}@{hostname}:{currentpath}$ '

    def __init__(self, nocoreutils=False, *args, **kwargs):
        if not nocoreutils:
            # Copy all commands from cmdix to 'do_foo' functions
            for command in cmdix.listcommands():
                x = """self.do_{0} = lambda l: \
                       cmdix.runcommandline('{0} '+ l)""".format(command)
                exec(x)
        return cmd.Cmd.__init__(self, *args, **kwargs)

    def default(self, line):
        """
        Called on an input line when the command prefix is not recognized.
        """
        ell = shlex.split(line)
        try:
            subprocess.call(ell)
        except OSError as err:
            if not os.path.dirname(ell[0]):
                # Scan $PATH
                if os.getenv('PATH'):
                    for path in os.getenv('PATH').split(':'):
                        cmd = [os.path.join(path, ell[0])] + ell[1:]
                        try:
                            subprocess.call(cmd)
                        except Exception:
                            pass

            print(err.strerror, file=sys.stderr)

    def do_cd(self, path):
        """
        Change directory
        """
        if not path:
            p = lib.getuserhome()
        else:
            p = os.path.expanduser(path)
        os.chdir(p)

    def do_exit(self, n=None):
        """
        Exit the shell.

        Exits the shell with a status of N.  If N is omitted, the exit status
        is that of the last command executed.
        """
        sys.exit(n or self.exitstatus)

    def do_help(self, arg):
        return (
            "Use 'COMMAND --help' for help\n"
            + "Available commands:\n"
            + ", ".join(cmdix.listcommands())
            + "\n"
        )

    def do_shell(self, line):
        """
        Run when them command is '!' or 'shell'.
        Execute the line using the Python interpreter.
        i.e. "!dir()"
        """
        try:
            exec(f"r = {line}")
        except Exception as err:
            return pprint.pformat(err) + '\n'
        else:
            return pprint.pformat(line) + '\n'

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt.
        """
        print()

    def postcmd(self, stop, line):
        self.updateprompt()
        if stop:
            for line in stop:
                print(line, end='')

    def onecmd(self, line):
        try:
            cmd.Cmd.onecmd(self, line)
        except SystemExit as exitstatus:
            try:
                self.exitstatus = int(exitstatus)
            except ValueError:
                self.exitstatus = 1
            except TypeError:
                self.exitstatus = 0
            else:
                self.exitstatus = 0

    def preloop(self):
        self.updateprompt()

    def updateprompt(self):
        """
        Update the prompt using format() on the template in self.prompttemplate

        You can use the following keywords:
        - currentpath
        - hostname
        - username
        """
        self.prompt = self.prompttemplate.format(
            currentpath=os.getcwd(),
            hostname=platform.node(),
            username=lib.getcurrentusername(),
        )
