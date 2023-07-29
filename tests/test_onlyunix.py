import os
import platform

import pytest

import cmdix
from cmdix import exception


@pytest.fixture
def pretend_windows(monkeypatch):
    monkeypatch.setattr(os, 'name', 'nt')
    monkeypatch.setattr(platform, 'system', lambda: 'Windows')


@pytest.mark.usefixtures('pretend_windows')
class TestCase:
    unix_only_cmds = (
        'chmod',
        'chown',
        'id',
        'mount',
        'tee',
        'uptime',
        'whoami',
    )

    def test_onlyunix(self):
        for command in self.unix_only_cmds:
            with pytest.raises(exception.CommandNotFoundException):
                cmdix.getcommand(command)
