import os

from .. import onlyunix
from .. import exception

try:
    import grp
    import pwd
except ImportError:
    pass


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: List all groups a user belongs to
    p.set_defaults(func=func)
    p.description = (
        "Print user and group information for the specified "
        + "USERNAME, or (when USERNAME omitted) for the current "
        + "user."
    )
    p.usage = '%(prog)s [OPTION]... [USERNAME]'
    p.add_argument('username', nargs='?')
    p.add_argument(
        "-a",
        action="store_true",
        dest="ignoreme",
        help="ignore, for compatibility with other versions",
    )
    p.add_argument(
        "-g",
        "--group",
        action="store_true",
        dest="group",
        help="print only the effective group ID",
    )
    p.add_argument(
        "-n",
        "--name",
        action="store_true",
        dest="name",
        help="print a name instead of a number, for -ug",
    )
    p.add_argument(
        "-u",
        "--user",
        action="store_true",
        dest="user",
        help="print only the effective group ID",
    )
    return p


def func(args):
    if args.username:
        u = pwd.getpwnam(args.username)
    else:
        u = pwd.getpwuid(os.getuid())

    uid = u.pw_uid
    gid = u.pw_gid
    username = u.pw_name
    g = grp.getgrgid(gid)
    groupname = g.gr_name

    if args.group and args.name:
        return groupname

    if args.group:
        return gid

    if args.user and args.name:
        return username

    if args.user:
        return uid

    if args.name:
        exception.StdErrException(
            "id: cannot print only names " + "or real IDs in default format"
        )

    print(f"uid={uid}({username}) gid={gid}({username})")
