from __future__ import print_function, unicode_literals
import platform


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "Print certain system information.  With no OPTION, " + \
                    "same as -s."
    p.add_argument(
        "-a", "--all", action="store_true", dest="all",
        help="print all information, in the following order, except "
        "omit -p and -i if unknown")
    p.add_argument(
        "-s", "--kernel-name", action="store_true",
        dest="kernelname", help="print the kernel name")
    p.add_argument(
        "-n", "--nodename", action="store_true", dest="nodename",
        help="print the network node hostname")
    p.add_argument(
        "-r", "--kernel-release", action="store_true",
        dest="kernelrelease", help="print the kernel release")
    p.add_argument(
        "-v", "--kernel-version", action="store_true",
        dest="kernelversion", help="print the kernel version")
    p.add_argument(
        "-m", "--machine", action="store_true", dest="machine",
        help="print the machine hardware name")
    p.add_argument(
        "-p", "--processor", action="store_true", dest="processor",
        help='print the processor type or "unknown"')
    p.add_argument(
        "-i", "--hardware-platform", action="store_true",
        dest="hardwareplatform",
        help="print the hardware platform or \"unknown\"")
    p.add_argument(
        "-o", "--operating-system", action="store_true",
        dest="operatingsystem", help="print the operating system")
    p.add_argument(
        "-A", "--architecture", action="store_true",
        dest="architecture", help="print the systems architecture")
    return p


def func(args):
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
        output.append(platform.processor())

    if args.hardwareplatform:
        # Didn't find a way to get this
        output.append('unknown')

    if args.architecture:
        output.append(" ".join(platform.architecture()))

    if args.operatingsystem or args.all or output == []:
        output.append(platform.system())

    print(" ".join(output))
