from .. import lib
import pydoc


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "number lines of files"
    p.add_argument('FILE', nargs='*')
    return p


def func(args):
    text = ''
    currentfilename = ''
    for line, filename in lib.parsefilelist(args.FILE):
        if len(args.FILE) > 1 and filename != currentfilename:
            currentfilename = filename
            text += "::::::::::::::\n"
            text += currentfilename + "\n"
            text += "::::::::::::::\n"
        text += line
    pydoc.pager(text)
