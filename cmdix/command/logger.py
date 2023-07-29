from ..exception import StdErrException
import logging


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: -i, -f, t
    p.set_defaults(func=func)
    p.description = "A shell command interface to the syslog system log " + "module"
    p.add_argument("message", nargs='?')
    p.add_argument(
        "--host",
        dest="host",
        help="Address of the syslog daemon. The default is 'localhost'",
    )
    p.add_argument(
        "-p",
        dest="priority",
        help="Enter the message with the specified priority. The "
        "priority may as a ''facility.level'' pair. For example, "
        "''-p local3.info'' logs the message(s) as informational "
        "level in the local3 facility. "
        "The default is ''user.notice.''",
    )
    p.add_argument(
        "--port", dest="port", help="Port of the syslog daemon. The default is 514'.'"
    )
    p.add_argument(
        "-s",
        action="store_true",
        dest="stderr",
        help="Log the message to standard error, as well as the " "system log.",
    )
    return p


def func(args):
    if args.priority:
        facility, level = args.priority.split('.', 2)
    else:
        facility = 'user'
        level = 'notice'

    if args.host or args.port:
        host = args.host or 'localhost'
        port = args.port or 514
        address = (host, port)
    else:
        address = '/dev/log'

    handler = logging.handlers.SysLogHandler(address, facility)
    if facility not in handler.facility_names:
        err = f"Unknown facility {facility}. " + "Valid facilities are: "
        facilitylist = list(handler.facility_names.keys())
        facilitylist.sort()
        for f in facilitylist:
            err += f + ", "

        raise StdErrException(err)

    msg = ' '.join(args.message)
    levelint = 90 - 10 * handler.priority_names.get(level, 0)

    logger = logging.getLogger('Logger')
    logger.addHandler(handler)
    logger.log(levelint, msg)

    if args.stderr:
        raise StdErrException(msg)
