#!/usr/bin/env python
from __future__ import unicode_literals
from . import BaseTestCase
import os
import unittest

import cmdix
from .. import exception


class TestCase(BaseTestCase):
    def test_onlyunix(self):
        for command in ['chmod', 'chown', 'id', 'ln', 'login', 'mount', 'tee',
                        'uptime', 'whoami']:
            os.name = 'nt'
            self.assertRaises(exception.CommandNotFoundException,
                              cmdix.getcommand, command)


if __name__ == '__main__':
    unittest.main()
