import gzip
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_cat(self):
        self.createfile('foo', size=66666)
        out = self.runcommandline('cat foo')[0]
        assert out == '0' * 66666

    def test_cat_gz(self):
        f = gzip.GzipFile('foo.gz', 'wb')
        f.write(b'0' * 12345)
        f.close()
        out = self.runcommandline('cat foo.gz')[0]
        assert out == '0' * 12345

    def test_cat_stdin(self):
        self.setStdin('foo' * 1000)
        out = self.runcommandline('cat')[0]
        assert out == 'foo' * 1000
