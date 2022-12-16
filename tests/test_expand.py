from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_expand(self):
        self.createfile('foo', fill='\t', size=100)
        out = self.runcommandline('expand foo')[0]
        assert out == ' ' * 100 * 8

    def test_expand_t(self):
        self.createfile('foo', fill='\t', size=100)
        out = self.runcommandline('expand -t 4 foo')[0]
        assert out == ' ' * 100 * 4
