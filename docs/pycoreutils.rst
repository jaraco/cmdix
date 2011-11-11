
PyCoreutils
===========

.. contents:: :local:

PyCoreutils is a pure Python implementation of various standard UNIX commands,
like `ls`, `tar` and `sleep`. It also contains a shell-like environment
which will make Unix-users feel right at home on the Windows command-prompt.

Since version 0.1.0, PyCoreutils also contains a modified version of
`Buildroot <http://buildroot.uclibc.org/>`_. This can be used to build a small
Linux distribution called :doc:`PyOS <pyos>`, which runs using pycoreutils.

Releases and documentation can be found at
http://pypi.python.org/pypi/pycoreutils.
The source code and bugtracker can be found at
https://launchpad.net/pycoreutils.


Download
--------

The downloads are located `here <http://pypi.python.org/pypi/pycoreutils#downloads>`_.


Install
-------

Pycoreutils requires Python 2.7 or 3.2, with bz2 and zlib modules.
To install the last stable version, use:

::

   $ easy_install pycoreutils

or

::

   $ pip install pycoreutils


To install the latest development version, try:

::

   $ pip install bzr+http://bazaar.launchpad.net/~hanz/pycoreutils/trunk


Generate Documenation
---------------------

To generate the html documentation in /build/sphinx/html, use:

::

   python setup.py build_docs
