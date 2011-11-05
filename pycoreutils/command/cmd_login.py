# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import crypt
import getpass
import os
import pwd
import spwd
import subprocess


@pycoreutils.onlyunix
def login(p):
    p.set_defaults(func=func)
    p.description = "Begin session on the system"
    p.add_argument("username", nargs="?")
    return p


def func(args):
    # Get username
    if args.username:
        username = args.username
    else:
        username = raw_input("Username: ")

    # Get password
    password = getpass.getpass("Password: ")

    # Authenticate
    try:
        # Get entry from /etc/shadow
        hashed_password = spwd.getspnam(username).sp_pwd
    except KeyError:
        print("Invalid username or password\n")
        func(args)
    else:
        if check_password(hashed_password, password):
            # Get entry from /etc/passwd
            pw = pwd.getpwnam(username)

            # Set UID of user
            os.setuid(pw.uid)

            # Change to homedir
            os.chdir(pw.pw_dir)

            # Set enviornment
            os.environ['USER'] = username
            os.environ['LOGNAME'] = username
            os.environ['HOME'] = pw.pw_dir
            os.environ['SHELL'] = pw.pw_shell

            # Start user shell
            subprocess.call([pw.pw_shell])
        else:
            print("Invalid username or password\n")


def check_password(hashed_password, password):
    salt = hashed_password.rsplit('$', 1)[0]
    return crypt.crypt(password, salt) == hashed_password
