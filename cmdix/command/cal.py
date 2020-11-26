from ..exception import ExtraOperandException
import calendar
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func, firstweekday=6)
    p.description = "Displays a calendar"
    p.usage = (
        '%(prog)s [OPTION]... [[MONTH] YEAR]\n'
        + '       %(prog)s -y [OPTION]... [YEAR]...'
    )
    p.add_argument('args', nargs='*')
    p.add_argument(
        "-M",
        action="store_const",
        dest="firstweekday",
        const=0,
        help="Weeks start on Monday",
    )
    p.add_argument(
        "-S",
        action="store_const",
        dest="firstweekday",
        const=6,
        help="Weeks start on Sunday",
    )
    p.add_argument(
        "-y",
        action="store_true",
        dest="year",
        help="Display a calendar for the specified year",
    )
    return p


def func(args):
    now = time.localtime()
    calen = calendar.TextCalendar(args.firstweekday)

    if args.year:
        if args.args != []:
            for arg in args.args:
                print(calen.formatyear(int(arg)), end='')
        else:
            print(calen.formatyear(now.tm_year), end='')
    else:
        if len(args.args) > 2:
            raise ExtraOperandException(args.prog, args.args[1])
        elif len(args.args) == 2:
            print(calen.formatmonth(int(args.args[1]), int(args.args[0])), end='')
        elif len(args.args) == 1:
            print(calen.formatyear(int(args.args[0])), end='')
        else:
            print(calen.formatmonth(now.tm_year, now.tm_mon), end='')
