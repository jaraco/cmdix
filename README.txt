***********
PyCoreutils
***********

What is this?
-------------

PyCoreutils is a pure Python implementation of various standard UNIX commands,
like 'ls', 'cp' and 'gzip'. It also contains sh.py, a shell-like environment
which will make Unix-users feel right at home on the Windows command-prompt.


Now why you wanna go and do that?
---------------------------------

1. Fun!
2. Have a Linux-like shell environment in Windows.
3. Create a Python-only Linux distribution.


Requirements
------------

PyCoreutils requires Python 2.6 or greater. It also works on Python 3.


Install
-------

To install the last stable version, use:

::

   pip install pycoreutils

or

::

   easy_install pycoreutils


To install the latest development code, try:

::

   pip install bzr+http://bazaar.launchpad.net/~hanz/pycoreutils/trunk


Downloads
---------

Releases and documentation can be found at http://pypi.python.org/pypi/pycoreutils.
The source code can be found at https://launchpad.net/pycoreutils.


Haven't I seen this before?
---------------------------

David Cantrell also has a project with the same name at
https://github.com/dcantrell/pycoreutils. His project is a little different
in that it uses C-bindings, is GPL-licensed and is structured differently.


License
-------

Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
See LICENSE.txt for details.


Warning
-------

This is alpha software, Not all the flags in the help-section are
implemented, and some behave different than one might expect.
