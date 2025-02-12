import datetime
import platform
import subprocess

import dateutil.parser


def parseargs(p):
    p.set_defaults(func=func)
    p.description = "Tell how long the system has been running"
    p.epilog = (
        "System load averages is the average number of processes "
        + "that are either in a runnable or uninterruptable state."
    )
    return p


def get_uptime_unix():
    with open('/proc/uptime') as f:
        uptimeseconds = float(f.readline().split()[0])
    uptime = str(datetime.timedelta(seconds=uptimeseconds))[:-10]
    return uptime


def get_loadavg_unix():
    with open('/proc/loadavg') as f:
        load5, load10, load15, proc, unknown = f.readline().split()[:5]
    return load5, load10, load15


def get_uptime_windows():
    process = subprocess.Popen('net stats workstation', stdout=subprocess.PIPE)
    stdout = process.communicate()[0].decode('utf-8')
    for line in stdout.split('\n'):
        if 'Statistics since' in line:
            start_time = line.split('Statistics since ')[1]
            start_time = dateutil.parser.parse(start_time)
            uptime = datetime.datetime.now() - start_time
            return str(uptime).split('.')[0]
    return None


def get_loadavg_windows():
    return 'N/A', 'N/A', 'N/A'


def func(args):
    if platform.system() == 'Windows':
        uptime = get_uptime_windows()
        load5, load10, load15 = get_loadavg_windows()
    else:
        uptime = get_uptime_unix()
        load5, load10, load15 = get_loadavg_unix()

    print(
        f" {datetime.datetime.now():%H:%M:%S} up "
        + " {},  {} users,  ".format(uptime, 'TODO')
        + f"load average: {load5}, {load10}, {load15}"
    )
