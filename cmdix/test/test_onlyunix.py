from __future__ import unicode_literals
import os

import pytest

import cmdix
from .. import exception


@pytest.fixture
def pretend_windows(monkeypatch):
    monkeypatch.setattr(os, 'name', 'nt')


@pytest.mark.usefixtures('pretend_windows')
class TestCase:
    unix_only_cmds = (
        'chmod', 'chown', 'id', 'login', 'mount', 'tee', 'uptime', 'whoami',
    )

    def test_onlyunix(self):
        for command in self.unix_only_cmds:
            with pytest.raises(exception.CommandNotFoundException):
                cmdix.getcommand(command)
