from ..hasher import hasher


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    return hasher('md5', p)
