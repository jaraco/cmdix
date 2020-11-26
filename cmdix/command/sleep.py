import time
import sys

from .. import exception


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "delay for a specified amount of time"
    p.epilog = (
        "Pause for NUMBER seconds. SUFFIX may be 's' for "
        + "seconds (the default), 'm' for minutes, 'h' for "
        + "hours or 'd' for days. Unlike most implementations "
        + "that require NUMBER be an integer, here NUMBER may "
        + "be an arbitrary floating point number. Given two or "
        + "more arguments, pause for the amount of time"
    )
    p.add_argument('number', nargs='+')
    return p


def func(args):
    a = []
    try:
        for arg in args.number:
            if arg.endswith('s'):
                a.append(float(arg[0:-1]))
            elif arg.endswith('m'):
                a.append(float(arg[0:-1]) * 60)
            elif arg.endswith('h'):
                a.append(float(arg[0:-1]) * 3600)
            elif arg.endswith('d'):
                a.append(float(arg[0:-1]) * 86400)
            else:
                a.append(float(arg))
    except ValueError:
        exception.StdErrException(
            "sleep: invalid time interval "
            "'{0}'. Try sleep --help' for more information.".format(arg)
        )
        sys.exit(1)

    time.sleep(sum(a))
