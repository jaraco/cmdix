"""
>>> import cmdix
>>> cmdix.runcommandline('sleep 0')
"""

import time


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
    p.add_argument('number', nargs='+', type=duration)
    return p


def duration(spec):
    """
    >>> duration('1')
    1.0
    >>> duration('1s')
    1.0
    >>> duration('1 s')
    1.0
    >>> duration('1h')
    3600.0
    >>> duration('1d')
    86400.0
    >>> duration('1m')
    60.0
    """
    if spec.endswith('s'):
        return float(spec[:-1])
    elif spec.endswith('m'):
        return float(spec[:-1]) * 60
    elif spec.endswith('h'):
        return float(spec[:-1]) * 3600
    elif spec.endswith('d'):
        return float(spec[:-1]) * 86400
    return float(spec)


def func(args):
    time.sleep(sum(args.number))
