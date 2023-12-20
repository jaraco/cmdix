import subprocess
import sys

import pytest

from . import BaseTestCase


issue15 = pytest.mark.xfail('platform.system() == "Windows"')


class TestCase(BaseTestCase):
    @issue15
    def test_env_dash_i(self, capfd):
        self.runcommandline('env -i FOO=bar env')
        assert capfd.readouterr().out == 'FOO=bar\n'

    @issue15
    def test_dash_as_dash_i(self, capfd):
        self.runcommandline('env - FOO=bar env')
        assert capfd.readouterr().out == 'FOO=bar\n'

    def test_env_simple(self, capfd):
        self.runcommandline('env')
        assert capfd.readouterr().out

    @issue15
    def test_command_opts(self, capfd):
        # invoke Python's help (not env's help)
        cmd = ['env', sys.executable, '--help']
        self.runcommandline(subprocess.list2cmdline(cmd))
        assert "-m mod" in capfd.readouterr().out
