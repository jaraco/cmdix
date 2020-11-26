from . import BaseTestCase

testdata = '''
foo bar

biz
 '''


class TestCase(BaseTestCase):
    def test_nl(self):
        self.createfile('foo', content=testdata)
        out = self.runcommandline('nl foo')[0]
        expected = '       \n     1\tfoo bar\n       \n     2\tbiz\n     3\t '
        assert out == expected

    def test_nl_s(self):
        self.createfile('foo', content=testdata)
        out = self.runcommandline('nl -s XYZ foo')[0]
        expected = '         \n     1XYZfoo bar\n         \n     2XYZbiz\n     3XYZ '
        assert out == expected

    def test_nl_w(self):
        self.createfile('foo', content=testdata)
        out = self.runcommandline('nl -w 2 foo')[0]
        assert out == '   \n 1\tfoo bar\n   \n 2\tbiz\n 3\t '
