from .. import lib
import os
import pathlib
import stat
import time


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: Show user and group names in ls -l, correctly format dates in ls -l
    p.set_defaults(func=func)
    p.description = (
        "List information about the FILEs (the current "
        + "directory by default). Sort entries "
        + "alphabetically if none of -cftuvSUX nor --sort."
    )
    p.add_argument('FILE', nargs="*")
    p.add_argument(
        "-l", "--longlist", action="store_true", help="use a long listing format"
    )
    p.add_argument(
        "-a",
        "--all",
        dest="filter",
        default=hide_dot,
        action="store_const",
        const=None,
        help="show all files",
    )
    return p


def hide_dot(path):
    return not path.name.startswith('.')


def resolve_items(arg):
    """
    Return a list of items in arg. If arg is a file, just return it.
    """
    if arg.is_file():
        return [arg]
    return arg.iterdir()


def func(args):
    filelist = args.FILE
    if not args.FILE:
        filelist = ['.']

    for arg in map(pathlib.Path, filelist):
        dirlist = sorted(resolve_items(arg))
        ell = []
        sizelen = 0  # Length of the largest filesize integer
        nlinklen = 0  # Length of the largest nlink integer
        for path in filter(args.filter, dirlist):
            if not args.longlist:
                print(path.name)
            else:
                st = os.lstat(path)
                mode = lib.mode2string(st.st_mode)
                nlink = st.st_nlink
                uid = st.st_uid
                gid = st.st_gid
                size = st.st_size
                mtime = time.localtime(st.st_mtime)
                name = (
                    f"{path.name} -> {path.readlink()}"
                    if stat.S_ISLNK(st.st_mode)
                    else path.name
                )
                ell.append((mode, nlink, uid, gid, size, mtime, name))

                # Update sizelen
                _sizelen = len(str(size))
                if _sizelen > sizelen:
                    sizelen = _sizelen

                # Update nlinklen
                _nlinklen = len(str(nlink))
                if _nlinklen > nlinklen:
                    nlinklen = _nlinklen

        for mode, nlink, uid, gid, size, mtime, name in ell:
            modtime = time.strftime('%Y-%m-%d %H:%m', mtime)
            print(
                "{0} {1:>{nlink}} {2:<5} {3:<5} {4:>{size}} {5} {6}".format(
                    mode,
                    nlink,
                    uid,
                    gid,
                    size,
                    modtime,
                    name,
                    size=sizelen,
                    nlink=nlinklen,
                )
            )
