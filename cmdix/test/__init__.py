from __future__ import print_function, unicode_literals

import filecmp
import os
import os.path
import sys

import pytest

import cmdix


if sys.version_info[0] == 2:
    from StringIO import StringIO
else:
    from io import StringIO


class BaseTestCase:

    def assertSamefile(self, file1, file2):
        assert filecmp.cmp(file1, file2)

    def createfile(self, filename, content=None, size=64 * 1024, fill='0'):
        '''
        Create a temporary file containing `content`. If `content` is not
        defined, fill file with `size` times `fill`.
        '''
        with open(os.path.join(self.workdir, filename), 'w') as fd:
            if content:
                fd.write(content)
            else:
                fd.write(size * fill)

    def createrandomfile(self, filename, size):
        '''
        Create a temporary file containing random data
        '''
        with open(os.path.join(self.workdir, filename), 'w') as fd:
            fd.write(os.urandom(size))

    def runcommandline(self, commandline, stdin=None):
        '''
        Run commandline as a subprocess.

        :param commandline: A string containing the commandline, i.e. 'ls -l X'
        :return:            A tuple containing the unicoded stdout and stderr
        '''
        stdoutio = StringIO()
        stderrio = StringIO()
        sys.stdout = stdoutio
        sys.stderr = stderrio
        cmdix.runcommandline(commandline)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdoutio.seek(0)
        stderrio.seek(0)
        stdoutstr = ''.join(stdoutio.readlines())
        stderrstr = ''.join(stderrio.readlines())
        return (stdoutstr, stderrstr)

    @pytest.fixture(autouse=True)
    def tmpdir_as_cwd(self, tmpdir):
        with tmpdir.as_cwd():
            self.workdir = str(tmpdir)
            yield tmpdir

    def setup_filesystem(self):
        '''
        Create the following filesystem:

        /dir1
        /dir1/dir1-1
        /dir1/dir1-1/dir1-1-1
        /dir1/dir1-1/dir1-1-1/file1-1-1-1
        /dir1/dir1-1/dir1-1-2
        /dir1/dir1-2
        /dir1/dir1-2/dir1-2-1
        /dir1/dir1-2/file1-2-1
        /dir1/dir1-2/file1-2-2
        /dir1/dir1-3
        /dir1/file1-1
        /dir1/file1-2
        /dir2
        /dir2/dir2-1
        /dir2/dir2-2
        /dir2/dir2-2/file2-2-1
        /file1
        /file2.txt
        /file3
        '''
        os.makedirs('dir1/dir1-1/dir1-1-1')
        os.makedirs('dir1/dir1-1/dir1-1-2')
        os.makedirs('dir1/dir1-2/dir1-2-1')
        os.makedirs('dir1/dir1-3')
        os.makedirs('dir2/dir2-1')
        os.makedirs('dir2/dir2-2')
        self.createfile('file1', size=111)
        self.createfile('file2.txt', size=2222)
        self.createfile('file3.empty', size=0)
        self.createfile('dir1/file1-1', size=33333)
        self.createfile('dir1/file1-2', size=44444)
        self.createfile('dir1/dir1-1/dir1-1-1/file1-1-1-1', size=55555)
        self.createfile('dir1/dir1-2/file1-2-1', size=66666)
        self.createfile('dir1/dir1-2/file1-2-2', size=77777)
        self.createfile('dir2/dir2-2/file2-2-1', size=88888)

    def setStdin(self, string):
        sys.stdin = StringIO(string)
