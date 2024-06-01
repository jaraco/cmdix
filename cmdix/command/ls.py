from .. import lib
import operator
import pathlib
import time
import types
from stat import S_ISLNK


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


class FileInfo(types.SimpleNamespace):
    @classmethod
    def from_path(cls, path):
        stat = path.lstat()
        return cls(
            mode=lib.mode2string(stat.st_mode),
            nlink=stat.st_nlink,
            uid=stat.st_uid,
            gid=stat.st_gid,
            size=stat.st_size,
            mtime=time.localtime(stat.st_mtime),
            name=(
                f"{path.name} -> {path.readlink()}"
                if S_ISLNK(stat.st_mode)
                else path.name
            ),
        )


def field_width(attr, infos):
    return max(map(len, map(str, map(operator.attrgetter(attr), infos))), default=0)


def func(args):
    filelist = args.FILE
    if not args.FILE:
        filelist = ['.']

    for arg in map(pathlib.Path, filelist):
        dirlist = sorted(resolve_items(arg))
        found = []
        for path in filter(args.filter, dirlist):
            if not args.longlist:
                print(path.name)
            else:
                found.append(FileInfo.from_path(path))

        sizelen = field_width('size', found)
        nlinklen = field_width('nlink', found)

        for info in found:
            modtime = time.strftime('%Y-%m-%d %H:%m', info.mtime)
            print(
                "{mode} {nlink:>{nlinklen}} {uid:<5} {gid:<5} {size:>{sizelen}} {modtime} {name}".format(
                    **vars(info), **locals()
                )
            )
