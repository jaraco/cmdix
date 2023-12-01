from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_env(self, capfd):
        self.runcommandline('env -i FOO=bar env')
        assert capfd.readouterr().out == 'FOO=bar\n'

    def test_env_simple(self, capfd):
        self.runcommandline('env')
        assert capfd.readouterr().out
