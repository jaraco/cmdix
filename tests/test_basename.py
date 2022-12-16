from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_basename(self, capsys):
        self.runcommandline('basename foo/bar/biz')
        assert capsys.readouterr().out == 'biz\n'
