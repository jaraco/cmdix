import os
import stat
import time
import textwrap
import pytest

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_ls(self, capsys):
        self.setup_filesystem()
        self.runcommandline('ls')
        assert capsys.readouterr().out == 'dir1\ndir2\nfile1\nfile2.txt\nfile3.empty\n'

    def test_ls_file(self, capsys):
        self.setup_filesystem()
        self.runcommandline('ls file2.txt')
        assert capsys.readouterr().out == 'file2.txt\n'

    @pytest.mark.xfail("platform.system() == 'Windows'")
    def test_ls_l(self, capsys):
        os.mkdir('biz', mode=0o755)
        self.createfile('foo', size=100)
        self.createfile('bar', size=999999)
        os.chmod('bar', stat.S_IWUSR + stat.S_IRGRP + stat.S_IWOTH + stat.S_IXOTH)
        os.chmod('foo', 0o644)

        dirsize = os.stat('biz').st_size
        uid = os.getuid()
        gid = os.getgid()
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        self.runcommandline('ls -l')
        expected = (
            textwrap.dedent(
                """
            --w-r---wx 1 {uid:<5} {gid:<5} 999999 {date} bar
            drwxr-xr-x 2 {uid:<5} {gid:<5} {dirsize:>6} {date} biz
            -rw-r--r-- 1 {uid:<5} {gid:<5}    100 {date} foo
            """
            )
            .lstrip()
            .format(**locals())
        )
        assert capsys.readouterr().out == expected
