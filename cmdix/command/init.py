import subprocess

import cmdix


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Process control initialization"
    return p


def func(args):
    # TODO: Create a real init-system
    mount()
    setHostname()
    cmdix.runcommandline('sh --nocoreutils')


def mount():
    subprocess.call(['/bin/mount', '-a'])


def setHostname():
    hostname = open('/etc/hostname').readline()
    open('/proc/sys/kernel/hostname', 'w').write(hostname)
