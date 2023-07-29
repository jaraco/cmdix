from .. import exception
import os
import signal

import cmdix


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = ""
    p.usage = '%(prog)s kill [ -SIGNAL | -s SIGNAL ] PID ...'
    p.add_argument("pid", nargs="+")
    p.add_argument(
        "-s",
        "--signal",
        action="store",
        dest="signal",
        default=signal.SIGTERM,
        help="send signal",
    )
    return p


def func(args):
    signals = cmdix.getsignals()

    # todo: fixme
    p = None

    add_arguments(p, signals)

    if len(args) == 0:
        raise exception.MissingOperandException(args.prog)

    try:
        sig = int(args.signal)
    except ValueError:
        sig = args.signal.upper()

    if list(signals.values()).count(sig):
        sigint = sig
    elif sig in signals:
        sigint = signals[sig]
    elif sig.lstrip('SIG') in signals:
        sigint = signals[sig.lstrip('SIG')]
    else:
        raise exception.StdErrException(f"kill: {sig}: invalid signal specification")

    for pid in args.pid:
        try:
            pid = int(pid)
        except ValueError:
            raise exception.StdErrException(
                f"kill: {pid}: arguments must be process or job IDs"
            )

        os.kill(pid, sigint)


def add_arguments(p, signals):
    # Add a string option for each signal
    for name, sigint in list(signals.items()):
        signame = 'SIG' + name.upper()
        p.add_argument(
            "--" + signame,
            action="store_const",
            dest="signal",
            const=sigint,
            help=f"send signal {signame}",
        )

    # Add an integer option for each signal
    for sigint in set(signals.values()):
        if sigint < 10:
            p.add_argument(
                "-%i" % sigint,
                action="store_const",
                dest="signal",
                const=sigint,
                help=f"send signal {sigint}",
            )
