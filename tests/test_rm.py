import pathlib

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_rm_f(self, capsys):
        self.setup_filesystem()
        pathlib.Path('dir1/file1-1').chmod(0o400)
        self.runcommandline('rm -rf dir1')
        assert capsys.readouterr().out == ''
