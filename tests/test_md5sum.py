from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self):
        self.createfile('foo')
        out = self.runcommandline('md5sum foo')[0]
        assert out == 'cf4b5c51a442990ed7304b535c9468c4  foo\n'
