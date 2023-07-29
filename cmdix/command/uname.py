import platform
import subprocess
import re
import contextlib


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = (
        "Print certain system information.  With no OPTION, " + "same as -s."
    )
    p.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="print all information, in the following order, except "
        "omit -p and -i if unknown",
    )
    p.add_argument(
        "-s",
        "--kernel-name",
        action="store_true",
        dest="kernelname",
        help="print the kernel name",
    )
    p.add_argument(
        "-n",
        "--nodename",
        action="store_true",
        dest="nodename",
        help="print the network node hostname",
    )
    p.add_argument(
        "-r",
        "--kernel-release",
        action="store_true",
        dest="kernelrelease",
        help="print the kernel release",
    )
    p.add_argument(
        "-v",
        "--kernel-version",
        action="store_true",
        dest="kernelversion",
        help="print the kernel version",
    )
    p.add_argument(
        "-m",
        "--machine",
        action="store_true",
        dest="machine",
        help="print the machine hardware name",
    )
    p.add_argument(
        "-p",
        "--processor",
        action="store_true",
        dest="processor",
        help='print the processor type or "unknown"',
    )
    p.add_argument(
        "-i",
        "--hardware-platform",
        action="store_true",
        dest="hardwareplatform",
        help="print the hardware platform or \"unknown\"",
    )
    p.add_argument(
        "-o",
        "--operating-system",
        action="store_true",
        dest="operatingsystem",
        help="print the operating system",
    )
    p.add_argument(
        "-A",
        "--architecture",
        action="store_true",
        dest="architecture",
        help="print the systems architecture",
    )
    return p


def processor_from_cpu_info():
    pattern = re.compile(r'model name\s+: (.*)')
    try:
        with open('/proc/cpuinfo') as lines:
            matched = next(filter(pattern.match, lines))
            return pattern.match(matched).group(1)
    except Exception:
        pass


def get_processor():
    """
    On Unix systems (or non-windows in particular), Python falls
    back to calling `uname -p` to get the processor... which
    won't work if this module is implementing uname. So find
    the info another way.
    """
    if platform.system() == 'Windows':
        return platform.processor()

    if platform.system() == 'Darwin':
        cmd = 'sysctl -n machdep.cpu.brand_string'.split()
        return subprocess.check_output(cmd, text=True).strip()

    return processor_from_cpu_info() or 'unknown'


@contextlib.contextmanager
def patch_syscmd_uname():
    """
    To prevent an infinite recursion when `platform.uname()` is called,
    suppress the `_syscmd_uname` function.
    """
    orig = getattr(platform, '_syscmd_uname', None)
    if not orig:
        yield
        return
    platform._syscmd_uname = lambda x, y: 'unknown'
    try:
        yield
    finally:
        platform._syscmd_uname = orig


def func(args):
    with patch_syscmd_uname():
        return do_it(args)


def do_it(args):
    output = []

    if args.kernelname or args.all:
        output.append(platform.system())

    if args.nodename or args.all:
        output.append(platform.node())

    if args.kernelrelease or args.all:
        output.append(platform.release())

    if args.kernelversion or args.all:
        output.append(platform.version())

    if args.machine or args.all:
        output.append(platform.machine())

    if args.processor:
        output.append(get_processor())

    if args.hardwareplatform:
        # Didn't find a way to get this
        output.append('unknown')

    if args.architecture:
        output.append(" ".join(platform.architecture()))

    if args.operatingsystem or args.all or output == []:
        output.append(platform.system())

    print(" ".join(output))
