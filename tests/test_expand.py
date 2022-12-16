from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_expand(self, capsys):
        self.createfile('foo', fill='\t', size=100)
        self.runcommandline('expand foo')
        assert capsys.readouterr().out == ' ' * 100 * 8

    def test_expand_t(self, capsys):
        self.createfile('foo', fill='\t', size=100)
        self.runcommandline('expand -t 4 foo')
        assert capsys.readouterr().out == ' ' * 100 * 4
