import gzip
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_cat(self, capsys):
        self.createfile('foo', size=66666)
        self.runcommandline('cat foo')
        assert capsys.readouterr().out == '0' * 66666

    def test_cat_gz(self, capsys):
        f = gzip.GzipFile('foo.gz', 'wb')
        f.write(b'0' * 12345)
        f.close()
        self.runcommandline('cat foo.gz')
        assert capsys.readouterr().out == '0' * 12345

    def test_cat_stdin(self, capsys):
        self.setStdin('foo' * 1000)
        self.runcommandline('cat')
        assert capsys.readouterr().out == 'foo' * 1000
