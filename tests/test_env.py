from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_env(self, capfd):
        self.runcommandline('env -i foo=bar env')
        assert capfd.readouterr().out == 'foo=bar\n'
