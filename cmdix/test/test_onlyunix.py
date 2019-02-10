#!/usr/bin/env python
from __future__ import unicode_literals
from . import BaseTestCase
import os
import unittest

import pytest

import cmdix
from .. import exception


@pytest.fixture
def pretend_windows(monkeypatch):
    monkeypatch.setattr(os, 'name', 'nt')


@pytest.mark.usefixtures('pretend_windows')
class TestCase(BaseTestCase):
    def test_onlyunix(self):
        for command in ['chmod', 'chown', 'id', 'ln', 'login', 'mount', 'tee',
                        'uptime', 'whoami']:
            self.assertRaises(exception.CommandNotFoundException,
                              cmdix.getcommand, command)


if __name__ == '__main__':
    unittest.main()
