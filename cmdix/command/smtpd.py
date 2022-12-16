import aiosmtpd.main


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.add_argument("-A", "--localaddress", default="", help="local address to bind to")
    p.add_argument(
        "-P", "--localport", default=25, type=int, help="local port to listen to"
    )
    return p


def func(args):
    aiosmtpd.main.main(
        ['--listen', f'{args.localaddress}:{args.localport}', '--nosetuid']
    )
