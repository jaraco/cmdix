v3.1.3
======

Bugfixes
--------

- Rewrite rm so it honors --force. (#17)


v3.1.2
======

Bugfixes
--------

- Add support for listing files by name. (#16)


v3.1.1
======

Bugfixes
--------

- env now honors ``-`` and options in the command (#14)


v3.1.0
======

Features
--------

- Implement support for env with subprocess. (#5)


v3.0.0
======

Features
--------

- Added support for ``ls -a``.
- Require Python 3.8 or later.


Deprecations and Removals
-------------------------

- Removed the login command, as it's based on deprecated and insecure libraries (crypt, spwd).


v2.0.2
======

#13: Fixed destination calculation in ``cp``.

v2.0.1
======

Fixed argument reference in ``cp``.

v2.0.0
======

Removed smtpd command, incompatible with Python 3.12.

v1.0.2
======

#12: Fixed argument reference in ``mv``.

v1.0.1
======

#12: Fixed argument handling in ``mv``.

v1.0.0
======

#10: Fixed argument handling in ``ln``.

v0.4.0
======

Refreshed packaging.

Require Python 3.7 or later.

v0.3.2
======

#4: Fixed broken commands: more, sort, sendmail.

v0.3.1
======

#3: Fixed argument handling in smtpd.

Fixed linter errors due to complexity checks.

Refreshed packaging.

v0.3.0
======

Require Python 3.6 or later.

Refreshed package metadata.

Test suite now passes on Windows.

v0.2.0
======

Removed createlinks command and now cmdix now installs
scripts unconditionally to the target environment.

v0.1.0
======

Initial release revived from pycoreutils.
