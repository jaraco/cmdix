import ctypes
import ctypes.util
import sys

from .. import onlyunix

# TODO: mount options


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    available_filesystems = get_available_filesystems()
    available_filesystems.sort()

    p.set_defaults(func=func)
    p.description = "Mount a filesystem"
    p.add_argument('SOURCE', nargs='?')
    p.add_argument('DEST', nargs='?')
    p.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Mount all filesystems mentioned in fstab",
    )
    # p.add_argument(
    #     "-o", "--options", default=0,
    #     help="print only the effective group ID")
    p.add_argument(
        "-t",
        "--types",
        default="ext2",
        help="Filesystem type. Supported types: " + ", ".join(available_filesystems),
    )
    p.add_argument(
        "-v", "--verbose", action="store_true", help="Output debugging information"
    )
    return p


def func(args):
    if args.SOURCE and args.DEST:
        mount_c(args.SOURCE, args.DEST, args.types, args.verbose)
    elif args.SOURCE or args.all:
        # Read fstab
        try:
            with open('/etc/fstab') as fd:
                lines = fd.readlines()
        except OSError:
            print("Error: Couldn't read /etc/ftab", file=sys.stderr)
            return

        # Mount filesystem
        mounted_something = False
        for line in lines:
            line = line.partition('#')[0]  # Remove comments
            source, dest, fstype, options, freq, passno = line.split()
            if source == args.SOURCE or dest == args.SOURCE or args.all:
                mount_c(dest, dest, fstype, args.verbose)
                mounted_something = True
        if not mounted_something:
            print(args.SOURCE + " not found in /etc/fstab", file=sys.stderr)
    else:
        # Display currently mounted filesystems
        try:
            print(open('/etc/mtab').read().strip())
        except OSError:
            print("Error: Couldn't read /etc/mtab", file=sys.stderr)


def mount_c(source, dest, fstype, options=0, data='', verbose=False):
    """
    Frontend to libc mount
    """
    if verbose:
        print(f"Trying to mount {source} on {dest} as type {fstype}")
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    res = libc.mount(str(source), str(dest), str(fstype), options, str(data))
    if res < 0:
        print(f"Error: Mounting {source} on {dest} failed!", file=sys.stderr)


def get_available_filesystems():
    try:
        with open('/proc/filesystems') as fd:
            return [line.split()[-1] for line in fd]
    except OSError:
        print(
            "Error reading supported filesystems from /proc/filesystems",
            file=sys.stderr,
        )
    return []
