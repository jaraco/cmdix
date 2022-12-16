from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_tail(self):
        self.createfile('foo', size=4096, fill='foo\n')
        assert self.runcommandline('tail foo')[0] == 'foo\n' * 10

    def test_tail_small(self):
        self.createfile('foo', size=4096, fill='foo\n')
        assert self.runcommandline('tail -n2 foo')[0] == 'foo\n' * 2
