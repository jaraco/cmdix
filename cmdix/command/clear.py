import curses
import sys


def parseargs(p):
    p.set_defaults(func=func)
    p.description = "Clear the terminal screen"
    return p


def func(args):
    curses.setupterm()
    sys.stdout.write(curses.tigetstr("clear"))
    sys.stdout.flush()
