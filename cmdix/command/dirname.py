import os.path


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Print NAME with its trailing /component removed; if "
        + "NAME contains no /'s, output '.' (meaning the current"
        + " directory)."
    )
    p.add_argument('path')
    return p


def func(args):
    d = os.path.dirname(args.path.rstrip('/'))
    if d == '':
        d = '.'
    return d + "\n"
