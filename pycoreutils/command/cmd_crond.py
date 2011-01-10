#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import collections
import fileinput
import logging
import sched
import subprocess
import sys
import time


@pycoreutils.addcommand
def crond(argstr):
    # TODO: Environment variables, different users and daemonize
    p = pycoreutils.parseoptions()
    p.description = "Very simple cron daemon"
    p.usage = "%prog [OPTION]... CRONFILE..."
    p.epilog = "If CRONFILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_option("-l", "--logfile", dest="logfile", help="log to file")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="show debug info")
    p.add_option("--dryrun", action="store_true", dest="dryrun",
            help="don't actually do anything")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if opts.logfile:
        logfile = open(opts.logfile, 'a')
    else:
        logfile = sys.stdout

    scheduler = sched.scheduler(time.time, time.sleep)
    joblist = []
    Job = collections.namedtuple('Job',
                                 'min, hour, mday, mon, wday, user, cmd')

    # Create logger
    logger = logging.getLogger("crond")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(logfile)
    handler.setFormatter(logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    # Read crontab and load jobs
    for line in fileinput.input(args):
        # Strip comments and split the string
        split = line.strip().partition('#')[0].split(None, 6)
        if len(split) == 7:
            job = Job(min=split[0], hour=split[1], mday=split[2],
                        mon=split[3], wday=split[4], user=split[5],
                        cmd=split[6])
            joblist.append(job)
            if opts.verbose:
                yield 'Read {0}'.format(job)
        elif split:
            yield 'Ignoring invalid line {0}'.format(line)

    def checkjobs():
        ''' Check if there are jobs available '''
        t = int(time.time() / 60 + 1) * 60  # start of the next minute
        scheduler.enterabs(t, 1, checkjobs, ())
        now = time.localtime(t)
        for job in joblist:
            if job.min in ['*', now.tm_min]    \
            and job.hour in ['*', now.tm_hour] \
            and job.mday in ['*', now.tm_mday] \
            and job.mon in ['*', now.tm_mon]   \
            and job.wday in ['*', now.tm_wday]:
                cmd = job.cmd
                if opts.verbose:
                    logger.info("Running job {0}".format(cmd))

                if opts.dryrun:
                    break

                # Run the command
                stdout, stderr = subprocess.Popen(cmd,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  shell=True).communicate()
                if opts.verbose:
                    if stdout:
                        logger.info("{0}: {1}".format(cmd, stdout.strip()))
                    if stderr:
                        logger.error("{0}: {1}".format(cmd, stderr.strip()))
            else:
                if opts.verbose:
                    logger.info("Skipping job {0}".format(job))

    scheduler.enter(1, 1, checkjobs, ())
    scheduler.run()
    raise pycoreutils.StdErrException("No more jobs. This should not happen!")
