import datetime

from .. import onlyunix


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    # TODO: List number of users
    p.set_defaults(func=func)
    p.description = "Tell how long the system has been running"
    p.epilog = (
        "System load averages is the average number of processes "
        + "that are either in a runnable or uninterruptable state."
    )
    return p


def func(args):
    with open('/proc/uptime') as f:
        uptimeseconds = float(f.readline().split()[0])
        uptime = str(datetime.timedelta(seconds=uptimeseconds))[:-10]

    with open('/proc/loadavg') as f:
        load5, load10, load15, proc, unknown = f.readline().split()[:5]
        totproc, avgproc = proc.split('/')

    print(
        " {0:%H:%M:%S} up ".format(datetime.datetime.today())
        + " {0},  {1} users,  ".format(uptime, 'TODO')
        + "load average: {0}, {1}, {2}".format(load5, load10, load15)
    )
