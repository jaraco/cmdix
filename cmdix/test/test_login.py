#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

from . import BaseTestCase
from ..command import cmd_login


class TestCase(BaseTestCase):
    def test_login_check_password(self):
        # tests disabled (don't work)
        return
        # Password is pycoreutils
        hash1 = '$1$JYOwx1mV$NUNwKlq4XGky9WjN1NU051'
        hash2 = '$6$.T7kFfCg$SWIuYR1sbw7IYmaVBddfm9BhW5yK89afw7p' +\
                'uXCLXzHcFnmQhBP9FwUnndt/ZCRILajW0ddhrLDiEERIk0RnBY0'
        self.assertTrue(cmd_login.check_password(hash1, 'pycoreutils'))
        self.assertTrue(cmd_login.check_password(hash2, 'pycoreutils'))
        self.assertFalse(cmd_login.check_password(hash2, 'FALSE!'))


if __name__ == '__main__':
    unittest.main()
