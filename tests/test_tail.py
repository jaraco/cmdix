from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_tail(self, capsys):
        self.createfile('foo', size=4096, fill='foo\n')
        self.runcommandline('tail foo')
        assert capsys.readouterr().out == 'foo\n' * 10

    def test_tail_small(self, capsys):
        self.createfile('foo', size=4096, fill='foo\n')
        self.runcommandline('tail -n2 foo')
        assert capsys.readouterr().out == 'foo\n' * 2
