from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self, capsys):
        self.createfile('foo')
        self.runcommandline('md5sum foo')
        assert capsys.readouterr().out == 'cf4b5c51a442990ed7304b535c9468c4  foo\n'
