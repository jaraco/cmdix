# Based on repeat.py by Guido van Rossum

import curses
import os
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "execute a program periodically, showing output fullscreen"
    p.add_argument('command', nargs='+')
    p.add_argument(
        "-n",
        "--interval",
        dest="seconds",
        type=float,
        default=2,
        help="Interval between updates",
    )
    return p


def func(args):
    cmd = " ".join(args.command)
    cmd_really = cmd + " 2>&1"
    p = os.popen(cmd_really, "r")
    text = p.read()
    sts = p.close()
    text = addsts(args.seconds, cmd, text, sts)
    w = curses.initscr()
    try:
        while True:
            w.erase()
            try:
                w.addstr(text)
            except curses.error:
                pass
            w.refresh()
            time.sleep(args.seconds)
            p = os.popen(cmd_really, "r")
            text = p.read()
            sts = p.close()
            text = addsts(args.seconds, cmd, text, sts)
    finally:
        curses.endwin()


def addsts(interval, cmd, text, sts):
    now = time.strftime("%H:%M:%S")
    text = f"{now}, every {interval:g} sec: {cmd}\n{text}"
    if sts:
        msg = "Exit status: %d; signal: %d" % (sts >> 8, sts & 0xFF)
        if text and not text.endswith("\n"):
            msg = "\n" + msg
        text += msg
    return text
