'''
Various helper-functions for .command
'''

import fileinput
import glob
import os
import signal
import stat
import sys
import textwrap

try:
    from backports.hook_compressed import hook_compressed
except ImportError:
    from fileinput import hook_compressed

import cmdix
from .compat import py39


def filelist2fds(filelist, mode='r'):
    """
    Take a list of files and yield the file descriptor.
    Yield sys.stdin if the filename is `-`, or the filelist is empty.
    Unix-style patterns will be parsed.

    So for example:::

       filelist2fds(["README.txt", "*.py", "-"])

    could yield:::

       <_io.TextIOWrapper name='README.txt' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='setup.py' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='test.py' mode='r' encoding='UTF-8'>
       <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>

    :param filelist: A list for files
    :param mode:     Mode in which the file is opened
    """
    filelist = filelist or ['-']
    for f in filelist:
        if f == '-':
            yield sys.stdin
        for filename in glob.iglob(f):
            if filename:
                encoding = None if 'b' in mode else 'utf-8'
                with open(filename, mode, encoding=encoding) as fd:
                    yield fd
            else:
                print(f"Cannot access {filename}: No such file or directory")


def getcurrentusername():
    """
    Returns the username of the current user
    """
    if 'USER' in os.environ:
        return os.environ['USER']  # Unix
    if 'USERNAME' in os.environ:
        return os.environ['USERNAME']  # Windows


def getsignals():
    """
    Return a dict of all available signals
    """
    signallist = [
        'ABRT',
        'CONT',
        'IO',
        'PROF',
        'SEGV',
        'TSTP',
        'USR2',
        '_DFL',
        'ALRM',
        'FPE',
        'IOT',
        'PWR',
        'STOP',
        'TTIN',
        'VTALRM',
        '_IGN',
        'BUS',
        'HUP',
        'KILL',
        'QUIT',
        'SYS',
        'TTOU',
        'WINCH',
        'CHLD',
        'ILL',
        'PIPE',
        'RTMAX',
        'TERM',
        'URG',
        'XCPU',
        'CLD',
        'INT',
        'POLL',
        'RTMIN',
        'TRAP',
        'USR1',
        'XFSZ',
    ]
    signals = {}
    for signame in signallist:
        if hasattr(signal, 'SIG' + signame):
            signals[signame] = getattr(signal, 'SIG' + signame)
    return signals


def getuserhome():
    """
    Returns the home-directory of the current user
    """
    if 'HOME' in os.environ:
        return os.environ['HOME']  # Unix
    if 'HOMEPATH' in os.environ:
        return os.environ['HOMEPATH']  # Windows


def _type(mode):
    if stat.S_ISREG(mode):
        return '-'
    elif stat.S_ISDIR(mode):
        return 'd'
    elif stat.S_ISCHR(mode):
        return 'c'
    elif stat.S_ISBLK(mode):
        return 'b'
    elif stat.S_ISLNK(mode):
        return 'l'
    elif stat.S_ISFIFO(mode):
        return 'p'
    elif stat.S_ISSOCK(mode):
        return 's'
    return '-'


def _read(mode, check):
    return 'r'


def mode2string(mode):
    """
    Convert mode-integer to string

    >>> from .lib import mode2string
    >>> mode2string(33261)
    '-rwxr-xr-x'
    >>> mode2string(33024)
    '-r--------'
    """

    s = _type(mode)
    s += 'r' if mode & stat.S_IRUSR else '-'
    s += 'w' if mode & stat.S_IWUSR else '-'
    s += 'x' if mode & stat.S_IXUSR else '-'
    s += 'r' if mode & stat.S_IRGRP else '-'
    s += 'w' if mode & stat.S_IWGRP else '-'
    s += 'x' if mode & stat.S_IXGRP else '-'
    s += 'r' if mode & stat.S_IROTH else '-'
    s += 'w' if mode & stat.S_IWOTH else '-'
    s += 'x' if mode & stat.S_IXOTH else '-'

    return s


def parsefilelist(filelist=None, decompress=False):
    r"""
    Take a list of files and generate a series of generators,
    each generating lines of a file.

    >>> import bz2
    >>> target = getfixture('tmpdir') / 'data.bz2'
    >>> target.write_binary(bz2.compress(b'Foo\nBar\nBiz'))
    >>> for filename in parsefilelist([str(target)], decompress=True):
    ...     for line in filename:
    ...         print(line.strip())
    Foo
    Bar
    Biz

    Files called `-` will be replaced with stdin.
    If decompress is defined, a file ending with `.gz` or `.bz2` is
    decompressed automatically.
    """
    openhook = hook_compressed if decompress else None

    # Use stdin if filelist is empty
    filelist = filelist or '-'

    for filename in filelist:
        yield fileinput.FileInput([filename], openhook=openhook, **py39.encoding)


def showbanner(width=None):
    """
    Returns the command banner.
    The banner is centered if width is defined.
    """
    subtext = f"-= Cmdix version {cmdix.__version__} =-"
    banner = textwrap.dedent(
        r"""
          ___  __  __  ____  ____  _  _
         / __)(  \/  )(  _ \(_  _)( \/ )
        ( (__  )    (  )(_) )_)(_  )  (
         \___)(_/\/\_)(____/(____)(_/\_)
        """
    ).lstrip('\n')

    if width:
        ret = ""
        for line in banner:
            ret += line.center(width) + "\n"
        ret += "\n" + subtext.center(width) + "\n"
        return ret
    else:
        return "\n".join(banner) + "\n\n" + subtext.center(68) + "\n"
