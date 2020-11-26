import crypt
import getpass
import os
import pwd
import subprocess
from multiprocessing import Process

from .. import onlyunix, run

try:
    import spwd
except ImportError:
    pass


@onlyunix
def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Begin session on the system"
    p.add_argument("username", nargs="?")
    return p


def func(args):
    while True:
        try:
            # Get username
            if args.username:
                username = args.username
            else:
                username = input("Username: ")

            # Get password
            password = getpass.getpass("Password: ")

            # Authenticate
            try:
                # Get entry from /etc/shadow
                hashed_password = spwd.getspnam(username).sp_pwd
            except KeyError:
                print("Invalid username or password\n")
                pass
            else:
                if check_password(hashed_password, password):
                    # Get entry from /etc/passwd
                    pw = pwd.getpwnam(username)

                    # Set UID of user
                    os.setuid(pw.pw_uid)

                    # Change to homedir
                    os.chdir(pw.pw_dir)

                    # Set enviornment
                    os.environ['USER'] = username
                    os.environ['LOGNAME'] = username
                    os.environ['HOME'] = pw.pw_dir
                    os.environ['SHELL'] = pw.pw_shell

                    # Start user shell
                    if pw.pw_shell == 'sh':
                        p = Process(target=run, args=[['sh']])
                        p.start()
                    else:
                        subprocess.call([pw.pw_shell])

                else:
                    print("Invalid username or password\n")
        except BaseException:
            print()


def check_password(hashed_password, password):
    salt = hashed_password.rsplit('$', 1)[0]
    return crypt.crypt(password, salt) == hashed_password
