import uuid


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "print a universally unique identifier (UUID)"
    p.add_argument(
        "-r",
        "--random",
        action="store_const",
        dest="uuidtype",
        const='RANDOM',
        help="Generate a random UUID",
    )
    p.add_argument(
        "-t",
        "--time",
        action="store_const",
        dest="uuidtype",
        const='TIME',
        help="Generate a UUID from a host ID, "
        + "sequence number, and the current time.",
    )
    return p


def func(args):
    if args.uuidtype == 'TIME':
        print(uuid.uuid1())
    else:
        print(uuid.uuid4())
