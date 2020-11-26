def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.add_argument('string', nargs='*', default=['y'])
    p.description = "Repeatedly output STRING"
    return p


def func(args):
    output = ' '.join(args.string)
    while 1:
        print(output)
