# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function
import pycoreutils
import os

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command


class CommandHelp(Command):
    description = "Create docs/comands.rst containing help for all commands"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root:%s' % self.cwd
        print("running build_commandhelp")
        with open('docs/commands.rst', 'w') as fd:
            fd.write("\nCommands\n========\n\n.. contents:: :local:\n")
            for commandname, commandhelp in pycoreutils.format_all_help():
                fd.write('\n\n' + commandname + '\n')
                fd.write('-' * len(commandname) + '\n\n')
                fd.write(commandhelp)


setup(
    name="pycoreutils",
    version=pycoreutils.__version__,
    description="Coreutils in Pure Python",
    long_description=pycoreutils.__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    license="MIT",
    url="http://pypi.python.org/pypi/pycoreutils",
    author="Hans van Leeuwen",
    author_email="hansvl@gmail.com",
    scripts=["scripts/pycoreutils"],
    packages=[
        "pycoreutils",
        "pycoreutils.command",
        "pycoreutils.test"
    ],
    test_suite="pycoreutils.test.getalltests",
    cmdclass={'build_commandhelp': CommandHelp},
)
