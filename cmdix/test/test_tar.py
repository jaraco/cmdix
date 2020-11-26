import tarfile

import pytest

from ..exception import StdErrException
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_notarfile(self):
        self.createfile('foo', size=100)
        with pytest.raises(StdErrException):
            self.runcommandline('tar -tf foo')

    def test_tar(self):
        self.setup_filesystem()
        good = [
            'dir1/',
            'dir1/dir1-1/',
            'dir1/dir1-1/dir1-1-1/',
            'dir1/dir1-1/dir1-1-1/file1-1-1-1',
            'dir1/dir1-1/dir1-1-2/',
            'dir1/dir1-2/',
            'dir1/dir1-2/dir1-2-1/',
            'dir1/dir1-2/file1-2-1',
            'dir1/dir1-2/file1-2-2',
            'dir1/dir1-3/',
            'dir1/file1-1',
            'dir1/file1-2',
            'dir2/',
            'dir2/dir2-1/',
            'dir2/dir2-2/',
            'dir2/dir2-2/file2-2-1',
            'file1',
        ]

        for archive in ('foo.tar', 'foo.tar.bz2', 'foo.tar.gz'):
            # Create an archive
            res = self.runcommandline('tar -cf {0} dir1 dir2 file1'.format(archive))
            assert res[0] == ''
            list_ = []
            for tarinfo in tarfile.open(archive):
                name = tarinfo.name
                if tarinfo.isdir():
                    name += '/'
                list_.append(name)
            list_.sort()
            assert list_ == good

            # List the archive
            x = self.runcommandline('tar -tf {0}'.format(archive))[0].split()
            x.sort()
            assert x == good

            # Extract the archive
            """
            d = os.getcwd()
            os.mkdir('extractdir')
            os.chdir('extractdir')
            x = self.runcommandline(
                    'tar -xf {0}'.format(os.path.join(d, archive)))[0].split()
            assert x == good
            """
