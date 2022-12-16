from . import BaseTestCase

testdata = '''
foo bar

biz
 '''


class TestCase(BaseTestCase):
    def test_nl(self, capsys):
        self.createfile('foo', content=testdata)
        self.runcommandline('nl foo')
        expected = '       \n     1\tfoo bar\n       \n     2\tbiz\n     3\t '
        assert capsys.readouterr().out == expected

    def test_nl_s(self, capsys):
        self.createfile('foo', content=testdata)
        self.runcommandline('nl -s XYZ foo')
        expected = '         \n     1XYZfoo bar\n         \n     2XYZbiz\n     3XYZ '
        assert capsys.readouterr().out == expected

    def test_nl_w(self, capsys):
        self.createfile('foo', content=testdata)
        self.runcommandline('nl -w 2 foo')
        assert capsys.readouterr().out == '   \n 1\tfoo bar\n   \n 2\tbiz\n 3\t '
