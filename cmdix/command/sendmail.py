import platform
import smtplib
import socket
import itertools

from .. import lib


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "A simple sendmail implementation"
    p.add_argument('recipient', nargs='*')
    p.add_argument(
        "-a",
        "--address",
        default="localhost",
        dest="address",
        help="address to send to. default is localhost",
    )
    p.add_argument(
        "-c",
        "--certfile",
        dest="certfile",
        help="certificate file to use. implies '-s'",
    )
    p.add_argument(
        "-f",
        "-r",
        "--sender",
        dest="sender",
        default=f"{lib.getcurrentusername()}@{platform.node()}",
        help="set the envelope sender address",
    )
    p.add_argument(
        "-k", "--keyfile", dest="keyfile", help="key file to use. implies '-s'"
    )
    p.add_argument(
        "-m",
        "--messagefile",
        default='-',
        dest="messagefile",
        help="read message from file. by default, read from stdin.",
    )
    p.add_argument(
        "-p",
        "--port",
        default=25,
        dest="port",
        type=int,
        help="port to send to. defaults is 25",
    )
    p.add_argument(
        "-t",
        "--timeout",
        default=socket._GLOBAL_DEFAULT_TIMEOUT,
        help="set timeout in seconds",
        dest="timeout",
        type=int,
    )
    p.add_argument(
        "-s", "--ssl", action="store_true", dest="ssl", help="connect using ssl"
    )
    p.add_argument(
        "-v", "--verbose", action="store_true", dest="verbose", help="show smtp session"
    )
    return p


def _read_msg(files):
    """
    >>> print(_read_msg([__file__]))
    import ...
    """
    return ''.join(itertools.chain.from_iterable(lib.parsefilelist(files)))


def func(args):
    # TODO: Authentication

    if args.ssl or args.certfile or args.keyfile:
        smtp = smtplib.SMTP_SSL(
            args.address,
            args.port,
            timeout=args.timeout,
            keyfile=args.keyfile,
            certfile=args.certfile,
        )
    else:
        smtp = smtplib.SMTP(args.address, args.port, timeout=args.timeout)

    smtp.set_debuglevel(args.verbose)
    smtp.sendmail(args.sender, args.recipient, _read_msg(args.messagefile))
    smtp.quit()
