import asyncore
import smtpd as _smtpd


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "An RFC 2821 smtp proxy."
    p.add_argument("-a", "--remoteaddress", help="remote address to connect to")
    p.add_argument(
        "-p", "--remoteport", default=25, type=int, help="remote port to connect to"
    )
    p.add_argument("-A", "--localaddress", default="", help="local address to bind to")
    p.add_argument(
        "-P", "--localport", default=25, type=int, help="local port to listen to"
    )
    return p


def func(args):
    _smtpd.SMTPServer(
        (args.localaddress, args.localport), (args.remoteaddress, args.remoteport)
    )

    asyncore.loop()
