import os
import types
from unittest import mock

import pytest

from cmdix.command import cp


@pytest.fixture
def mocked_dirs(monkeypatch):
    dirs = set()
    real_isdir = os.path.isdir

    def is_dir(cand):
        return real_isdir(cand) or cand in dirs

    monkeypatch.setattr(os.path, 'isdir', is_dir)

    return dirs


def test_simple_cp_with_dest(mocked_dirs):
    args = types.SimpleNamespace(verbose=False)
    copy_fn = mock.Mock()
    mocked_dirs.add('foo/bar')
    cp.handle_direct(_copy=copy_fn, args=args, dest='foo/bar', src='/baz/bing.py')
    expected_dest = os.path.join('foo/bar', 'bing.py')
    copy_fn.assert_called_with('/baz/bing.py', expected_dest)
